import './chat.css';

export type ChatOption = { id: string; text: string; label: string; emoji: string };
export type ChatSample = {
  id: string;
  state: string;
  question: string;
  options: ChatOption[];
};
export type ChatPrediction = {
  probabilities: { option_id: string; probability: number }[];
};
type Config = {
  samples: ChatSample[];
  question: string;
  options: ChatOption[];
  predict: (sample: ChatSample) => Promise<ChatPrediction>;
};
type Message = {
  sample: ChatSample;
  revision: string;
  pending: boolean;
  result?: ChatPrediction;
  error?: string;
  override?: string;
  dismissed: boolean;
  article: HTMLElement;
  body: HTMLElement;
  actions: HTMLElement;
  edit: HTMLButtonElement;
};

function element<K extends keyof HTMLElementTagNameMap>(tag: K, cls: string, text?: string) {
  const node = document.createElement(tag);
  node.className = cls;
  if (text !== undefined) node.textContent = text;
  return node;
}
function button(text: string, action: () => void, cls = 'chat-action') {
  const node = element('button', cls, text);
  node.type = 'button';
  node.addEventListener('click', action);
  return node;
}
function copySample(sample: ChatSample): ChatSample {
  return {
    id: sample.id, state: sample.state, question: sample.question,
    options: sample.options.map(option => ({ ...option })),
  };
}
function checkedPrediction(value: ChatPrediction, options: ChatOption[]): ChatPrediction {
  const rows = value?.probabilities;
  const ids = new Set(options.map(option => option.id));
  if (!options.length || ids.size !== options.length || !Array.isArray(rows) || rows.length !== options.length ||
    new Set(rows.map(row => row.option_id)).size !== rows.length || rows.some(row =>
      !ids.has(row.option_id) || !Number.isFinite(row.probability) || row.probability < 0 || row.probability > 1) ||
    Math.abs(rows.reduce((sum, row) => sum + row.probability, 0) - 1) > 0.000001) {
    throw new Error('Invalid prediction');
  }
  return { probabilities: rows.map(row => ({ ...row })) };
}

export function mountChat(root: HTMLElement, config: Config): {
  dispose(): void;
} {
  let disposed = false;
  const messages: Message[] = [];
  const options = config.options.map(option => ({ ...option }));
  const question = config.question;
  const predict = config.predict;
  const shell = element('section', 'chat-demo');
  shell.setAttribute('aria-label', 'Message reactions');
  const header = element('header', 'chat-header');
  const heading = element('div', 'chat-heading');
  heading.append(element('span', 'chat-channel-mark', '#'), element('h2', 'chat-title', 'Reactions'));
  header.append(heading, element('p', 'chat-subtitle', 'Messages, with room for a reaction.'));
  const transcript = element('div', 'chat-transcript');
  transcript.setAttribute('role', 'region');
  transcript.setAttribute('aria-label', 'Messages');
  transcript.tabIndex = 0;
  const intro = element('aside', 'chat-intro');
  intro.append(element('span', 'chat-system-mark', '↳'), element('p', '', 'Write a message to compare its sentiment.'));
  transcript.append(intro);
  const form = element('form', 'chat-composer');
  const label = element('label', 'chat-composer-label', 'Your message');
  const input = element('textarea', 'chat-input');
  input.rows = 3;
  input.placeholder = 'What would you like to say?';
  input.setAttribute('aria-label', 'Your message');
  label.append(input);
  const footer = element('div', 'chat-composer-footer');
  const hint = element('span', 'chat-hint', 'Ctrl / ⌘ + Enter to send');
  const send = element('button', 'chat-send', 'Send message ↑');
  send.type = 'submit';
  send.disabled = true;
  const composeError = element('p', 'chat-error');
  composeError.setAttribute('role', 'alert');
  composeError.hidden = true;
  footer.append(hint, send);
  form.append(label, footer, composeError);
  shell.append(header, transcript, form);
  root.append(shell);

  function renderActions(message: Message) {
    const hadFocus = message.actions.contains(document.activeElement);
    message.actions.replaceChildren();
    message.article.setAttribute('aria-busy', String(message.pending));
    const status = element('span', 'chat-status');
    status.setAttribute('role', 'status');
    if (message.pending) {
      status.classList.add('chat-loading');
      status.textContent = 'Finding a reaction…';
      message.actions.append(status);
    } else if (message.error) {
      status.classList.add('chat-error');
      status.textContent = message.error;
      message.actions.append(status, button('Retry suggestion', () => { void suggest(message); }));
    } else if (!message.result) {
      message.actions.append(button('Suggest reaction', () => { void suggest(message); }));
    } else {
      const result = message.result;
      const max = Math.max(...result.probabilities.map(row => row.probability));
      const winners = message.sample.options.filter(option => result.probabilities.some(row => row.option_id === option.id && row.probability === max));
      const selected = message.override ? message.sample.options.find(option => option.id === message.override) : winners.length === 1 ? winners[0] : undefined;
      const details = element('details', 'chat-details');
      const summary = element('summary', 'chat-reaction');
      const interpretation = message.override ? `Your choice · ${selected?.label ?? ''}` : winners.length > 1 ? `Ambiguous · tied: ${winners.map(option => option.label).join(', ')}` : `Model suggestion · ${selected?.label ?? ''}`;
      summary.textContent = message.dismissed ? 'View suggestion' : selected ? `${selected.emoji} ${selected.label}` : 'Tied suggestion';
      summary.title = interpretation;
      summary.setAttribute('aria-label', `${interpretation}. View scores and reaction actions`);
      const panel = element('div', 'chat-reaction-panel');
      panel.append(element('p', 'chat-interpretation', interpretation), element('p', 'chat-score-note', 'Relative scores · not confidence'));
      const scores = element('dl', 'chat-scores');
      for (const option of message.sample.options) {
        const row = result.probabilities.find(value => value.option_id === option.id)!;
        scores.append(element('dt', '', option.label), element('dd', '', `${(row.probability * 100).toFixed(1)}%`));
      }
      const choiceLabel = element('label', 'chat-choice-label', 'Choose your own reaction');
      const choice = element('select', 'chat-select');
      const placeholder = element('option', '', 'Select a reaction…');
      placeholder.value = '';
      choice.append(placeholder);
      for (const option of message.sample.options) {
        const item = element('option', '', `${option.emoji} ${option.label}`);
        item.value = option.id;
        choice.append(item);
      }
      choice.value = message.override ?? '';
      choice.addEventListener('change', () => {
        if (!choice.value || disposed) return;
        message.override = choice.value;
        message.dismissed = false;
        renderActions(message);
      });
      choiceLabel.append(choice);
      panel.append(scores, choiceLabel, button(message.dismissed ? 'Restore suggestion' : 'Dismiss reaction', () => {
        message.dismissed = !message.dismissed;
        message.override = undefined;
        renderActions(message);
      }));
      details.append(summary, panel);
      message.actions.append(details);
      if (message.override && !message.dismissed) message.actions.append(element('span', 'chat-status', 'Your choice'));
      if (message.dismissed) message.actions.append(element('span', 'chat-status', 'Reaction dismissed'));
    }
    if (hadFocus) (message.actions.querySelector<HTMLElement>('button, summary') ?? message.edit).focus();
  }

  async function suggest(message: Message) {
    if (disposed || message.pending) return;
    const revision = message.revision;
    message.pending = true;
    message.error = undefined;
    renderActions(message);
    try {
      // The callback receives an isolated snapshot; edits never mutate an in-flight input.
      const value = await predict(copySample(message.sample));
      if (disposed || message.revision !== revision) return;
      message.result = checkedPrediction(value, message.sample.options);
      message.override = undefined;
      message.dismissed = false;
    } catch (error) {
      if (disposed || message.revision !== revision) return;
      message.error = error instanceof Error ? error.message : 'Couldn’t get a suggestion. Your message is still here.';
    } finally {
      if (!disposed && message.revision === revision) {
        message.pending = false;
        renderActions(message);
      }
    }
  }

  function startEditing(message: Message) {
    if (disposed || message.body.querySelector('textarea')) return;
    const editor = element('textarea', 'chat-edit-input');
    editor.value = message.sample.state;
    editor.rows = 3;
    editor.setAttribute('aria-label', 'Edit your message');
    const controls = element('div', 'chat-edit-controls');
    const error = element('p', 'chat-error');
    error.setAttribute('role', 'alert');
    const cancel = () => { message.body.replaceChildren(element('p', 'chat-message-text', message.sample.state)); message.edit.focus(); };
    const save = () => {
      if (!editor.value.trim()) { error.textContent = 'Write a message before saving.'; editor.focus(); return; }
      if (editor.value.trim() !== message.sample.state) {
        let revision: string;
        try { revision = crypto.randomUUID(); } catch { error.textContent = 'Secure message IDs are unavailable in this context.'; return; }
        message.revision = revision;
        message.sample = { ...message.sample, id: revision, state: editor.value.trim() };
        message.result = undefined;
        message.error = undefined;
        message.pending = false;
        message.override = undefined;
        message.dismissed = false;
        message.article.dataset.revisionId = revision;
        renderActions(message);
      }
      cancel();
    };
    editor.addEventListener('keydown', event => {
      if (event.key === 'Escape') { event.preventDefault(); cancel(); }
      if (event.key === 'Enter' && (event.ctrlKey || event.metaKey) && !event.isComposing) { event.preventDefault(); save(); }
    });
    controls.append(button('Save edit', save), button('Cancel', cancel));
    message.body.replaceChildren(editor, controls, error);
    editor.focus();
  }

  function append(sample: ChatSample, supplied: boolean): Message {
    const article = element('article', 'chat-message');
    article.dataset.messageId = sample.id;
    article.dataset.revisionId = sample.id;
    const avatar = element('div', 'chat-avatar', supplied ? '·' : 'Y');
    avatar.setAttribute('aria-hidden', 'true');
    const content = element('div', 'chat-message-content');
    const meta = element('div', 'chat-meta');
    meta.append(element('span', 'chat-author', supplied ? 'Message' : 'You'));
    const body = element('div', 'chat-message-body');
    body.append(element('p', 'chat-message-text', sample.state));
    const actions = element('div', 'chat-message-actions');
    const edit = button('Edit', () => startEditing(message), 'chat-edit');
    meta.append(edit);
    content.append(meta, body, actions);
    article.append(avatar, content);
    const message: Message = { sample: copySample(sample), revision: sample.id, pending: false, dismissed: false, article, body, actions, edit };
    messages.push(message);
    renderActions(message);
    transcript.append(article);
    return message;
  }
  for (const sample of config.samples) append(sample, true);

  function updateComposer() {
    send.disabled = !input.value.trim();
    composeError.hidden = true;
    input.removeAttribute('aria-invalid');
  }
  function submit(event: Event) {
    event.preventDefault();
    if (disposed || !input.value.trim()) return;
    let id: string;
    try { id = crypto.randomUUID(); } catch {
      composeError.textContent = 'Couldn’t create a secure message ID. Your draft has not been sent.';
      composeError.hidden = false;
      input.setAttribute('aria-invalid', 'true');
      input.focus();
      return;
    }
    const message = append({ id, state: input.value.trim(), question, options }, false);
    input.value = '';
    updateComposer();
    input.focus();
    transcript.scrollTop = transcript.scrollHeight;
    void suggest(message);
  }
  function shortcut(event: KeyboardEvent) {
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey) && !event.isComposing) submit(event);
  }
  input.addEventListener('input', updateComposer);
  input.addEventListener('keydown', shortcut);
  form.addEventListener('submit', submit);
  return {
    dispose() {
      if (disposed) return;
      disposed = true;
      input.removeEventListener('input', updateComposer);
      input.removeEventListener('keydown', shortcut);
      form.removeEventListener('submit', submit);
      input.value = '';
      for (const message of messages) {
        message.sample.state = '';
        message.result = undefined;
        message.body.replaceChildren();
        message.actions.replaceChildren();
      }
      messages.length = 0;
      shell.remove();
    },
  };
}
