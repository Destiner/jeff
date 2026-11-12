import './queue.css';

export type QueueOption = { id: string; text: string; label: string };
export type QueueSample = {
  id: string;
  title: string;
  state: string;
  question: string;
  options: QueueOption[];
};
export type QueuePrediction = {
  probabilities: { option_id: string; probability: number }[];
};

type RecordState = {
  originalId: string;
  sample: QueueSample;
  revision: number;
  pending: boolean;
  request: number;
  prediction?: QueuePrediction;
  error: string;
  destination: string;
  routed: boolean;
};

export function mountQueue(
  root: HTMLElement,
  config: {
    samples: QueueSample[];
    predict: (sample: QueueSample) => Promise<QueuePrediction>;
    onChange?: () => void;
  },
): { dispose(): void } {
  const doc = root.ownerDocument;
  let disposed = false;
  let serial = 0;
  const mountId = `queue-${globalThis.crypto.randomUUID()}`;
  const records: RecordState[] = config.samples.map(sample => ({
    originalId: sample.id,
    sample: clone(sample),
    revision: 0,
    pending: false,
    request: 0,
    error: '',
    destination: '',
    routed: false,
  }));
  let selected = records[0];
  let query = '';
  let filter = 'all';

  function el<K extends keyof HTMLElementTagNameMap>(tag: K, cls = '', text?: string) {
    const node = doc.createElement(tag);
    node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function button(text: string, cls: string, action: () => void) {
    const node = el('button', cls, text);
    node.type = 'button';
    node.addEventListener('click', action);
    return node;
  }
  function clone(sample: QueueSample): QueueSample {
    return {
      ...sample,
      options: sample.options.map(option => ({ ...option })),
    };
  }
  function notify() { config.onChange?.(); }

  const shell = el('section', 'queue-demo');
  shell.setAttribute('aria-label', 'Request queue');
  const header = el('header', 'queue-header');
  const brand = el('div', 'queue-brand');
  brand.append(el('span', 'queue-brand-mark', 'J'), el('span', '', 'Jeff'));
  header.append(brand, el('span', 'queue-header-divider'), el('span', 'queue-header-label', 'Workspace routing'));
  const heading = el('div', 'queue-heading');
  const headingCopy = el('div');
  headingCopy.append(el('p', 'queue-eyebrow', 'WORKSPACE'), el('h1', '', 'Request queue'));
  const summary = el('span', 'queue-summary');
  heading.append(headingCopy, summary);
  const workspace = el('div', 'queue-workspace');
  const left = el('section', 'queue-list-panel');
  left.setAttribute('aria-label', 'Requests');
  const tools = el('div', 'queue-tools');
  const searchLabel = el('label', 'queue-search');
  searchLabel.append(el('span', 'queue-sr-only', 'Search requests'));
  const search = el('input');
  search.type = 'search';
  search.placeholder = 'Search requests…';
  searchLabel.append(search);
  const filterLabel = el('label', 'queue-filter-label');
  filterLabel.append(el('span', 'queue-sr-only', 'Filter requests'));
  const filterSelect = el('select', 'queue-filter');
  for (const [value, text] of [['all', 'All requests'], ['open', 'Unrouted'], ['routed', 'Routed']] as const) {
    const option = el('option', '', text);
    option.value = value;
    filterSelect.append(option);
  }
  filterLabel.append(filterSelect);
  tools.append(searchLabel, filterLabel);
  const count = el('div', 'queue-list-caption');
  const list = el('div', 'queue-list');
  left.append(tools, count, list);
  const detail = el('section', 'queue-detail');
  detail.setAttribute('aria-label', 'Selected request');
  workspace.append(left, detail);
  const live = el('div', 'queue-sr-only');
  live.setAttribute('role', 'status');
  live.setAttribute('aria-live', 'polite');
  shell.append(header, heading, workspace, live);
  root.append(shell);

  function visibleRecords() {
    const term = query.trim().toLocaleLowerCase();
    return records.filter(record =>
      (filter === 'all' || (filter === 'routed' ? record.routed : !record.routed)) &&
      (!term || [record.sample.title, record.sample.state, record.sample.question]
        .some(text => text.toLocaleLowerCase().includes(term))),
    );
  }
  function renderList() {
    const visible = visibleRecords();
    summary.textContent = `${records.filter(record => !record.routed).length} unrouted · ${records.length} total`;
    count.textContent = `${visible.length} ${visible.length === 1 ? 'request' : 'requests'}`;
    list.replaceChildren();
    if (!visible.length) {
      list.append(el('p', 'queue-empty', 'No matching requests. Try another search or filter.'));
      return;
    }
    for (const record of visible) {
      const row = button('', 'queue-row', () => {
        selected = record;
        renderList();
        renderDetail();
        const activeRow = Array.from(list.querySelectorAll<HTMLButtonElement>('button'))
          .find(node => node.dataset.record === record.originalId);
        activeRow?.focus({ preventScroll: true });
        notify();
      });
      row.dataset.record = record.originalId;
      row.setAttribute('aria-pressed', String(selected === record));
      const top = el('span', 'queue-row-top');
      top.append(el('span', 'queue-row-title', record.sample.title || 'Untitled request'));
      const status = record.routed
        ? `Routed to ${record.sample.options.find(option => option.id === record.destination)?.label ?? 'destination'}`
        : 'Unrouted';
      top.append(el('span', `queue-status${record.routed ? ' queue-status-routed' : ''}`, status));
      row.append(top, el('span', 'queue-row-preview', record.sample.state || record.sample.question));
      const bottom = el('span', 'queue-row-bottom');
      bottom.append(el('span', '', record.revision ? 'Edited request' : 'Request'));
      if (record.prediction) bottom.append(el('span', '', 'Suggestion available'));
      row.append(bottom);
      list.append(row);
    }
  }

  function renderDetail() {
    const active = doc.activeElement;
    const focusId = active && detail.contains(active) ? active.id : '';
    detail.replaceChildren();
    if (!selected) {
      detail.append(el('div', 'queue-empty', 'Select a request to choose its destination.'));
      return;
    }
    const record = selected;
    const sample = record.sample;
    const top = el('div', 'queue-detail-top');
    const detailStatus = el('span', 'queue-status', record.routed ? 'Routed' : 'Unrouted');
    top.append(el('span', 'queue-eyebrow', 'REQUEST'), detailStatus);
    const title = el('h2', 'queue-detail-title', sample.title || 'Untitled request');
    const editorLabel = el('label', 'queue-field-label', 'Request text');
    const editor = el('textarea', 'queue-editor');
    editor.id = `${mountId}-text`;
    editorLabel.htmlFor = editor.id;
    editor.value = sample.state;
    editor.rows = 6;
    editor.spellcheck = false;
    const editHint = el('p', 'queue-field-hint', 'Editing clears the suggestion and route confirmation.');
    editor.setAttribute('aria-describedby', `${mountId}-edit-hint`);
    editHint.id = `${mountId}-edit-hint`;
    const question = el('div', 'queue-question');
    question.append(el('span', 'queue-field-label', 'Decision'), el('p', '', sample.question));
    const suggestion = el('section', 'queue-suggestion');
    suggestion.setAttribute('aria-label', 'Model suggestion');
    const suggestionTop = el('div', 'queue-section-heading');
    suggestionTop.append(el('h3', '', 'Model suggestion'));
    const suggestButton = button(record.pending ? 'Getting suggestion…' : record.prediction ? 'Suggest again' : 'Suggest destination', 'queue-button queue-button-secondary', () => {
      if (!record.pending) void predict(record);
    });
    suggestButton.id = `${mountId}-suggest`;
    suggestButton.setAttribute('aria-disabled', String(record.pending));
    suggestionTop.append(suggestButton);
    suggestion.append(suggestionTop);
    const result = el('div', 'queue-result');
    result.setAttribute('aria-busy', String(record.pending));
    const route = el('section', 'queue-route');
    route.setAttribute('aria-label', 'Route request');
    route.append(el('h3', '', 'Destination'));
    const routeHint = el('p', 'queue-field-hint', 'Choose where this request should go.');
    const destinationLabel = el('label', 'queue-sr-only', 'Destination workspace');
    const destinationSelect = el('select', 'queue-destination');
    destinationSelect.id = `${mountId}-destination`;
    destinationLabel.htmlFor = destinationSelect.id;
    const placeholder = el('option', '', 'Select destination…');
    placeholder.value = '';
    destinationSelect.append(placeholder);
    for (const option of sample.options) {
      const choice = el('option', '', option.label);
      choice.value = option.id;
      destinationSelect.append(choice);
    }
    destinationSelect.value = record.destination;
    const routeButton = button('Route request', 'queue-button queue-button-primary', () => {
      if (!record.destination) return;
      record.routed = true;
      renderList();
      updateRoute();
      live.textContent = `Request routed to ${sample.options.find(option => option.id === record.destination)?.label}.`;
      notify();
    });
    routeButton.id = `${mountId}-route`;
    const routeControls = el('div', 'queue-route-controls');
    const routeStatus = el('p', 'queue-route-status');
    routeStatus.setAttribute('role', 'status');
    routeControls.append(destinationSelect, routeButton);
    route.append(routeHint, destinationLabel, routeControls, routeStatus);
    detail.append(top, title, editorLabel, editor, editHint, question, suggestion, route);

    function updateRoute() {
      detailStatus.textContent = record.routed ? 'Routed' : 'Unrouted';
      routeButton.disabled = !record.destination || record.routed;
      routeButton.textContent = record.routed ? 'Routed' : 'Route request';
      routeStatus.textContent = record.routed
        ? `Routed to ${sample.options.find(option => option.id === record.destination)?.label}.`
        : '';
    }
    function updateResult() {
      result.replaceChildren();
      if (record.error) {
        const error = el('p', 'queue-error', record.error);
        error.setAttribute('role', 'alert');
        result.append(error);
      } else if (record.pending) {
        result.append(el('p', 'queue-field-hint', 'Waiting for the model result…'));
      } else if (!record.prediction) {
        result.append(el('p', 'queue-field-hint', 'Ask for a suggestion, or choose a destination directly.'));
      } else {
        const scores = record.prediction.probabilities;
        const maximum = Math.max(...scores.map(score => score.probability));
        const leaders = sample.options.filter(option => scores.find(score => score.option_id === option.id)!.probability === maximum);
        result.append(el('p', 'queue-result-heading', leaders.length > 1
          ? `Tied: ${leaders.map(option => option.label).join(' / ')}`
          : `Suggested: ${leaders.map(option => option.label).join('')}`));
        result.append(el('p', 'queue-score-caption', 'Relative scores · not confidence'));
        for (const option of sample.options) {
          const probability = scores.find(score => score.option_id === option.id)!.probability;
          const score = el('div', 'queue-score');
          const label = el('div', 'queue-score-label');
          const formatted = `${(probability * 100).toFixed(1)}%`;
          label.append(el('span', '', option.label), el('span', 'queue-score-value', formatted));
          const track = el('div', 'queue-score-track');
          track.setAttribute('aria-hidden', 'true');
          const fill = el('span', 'queue-score-fill');
          fill.style.width = `${probability * 100}%`;
          track.append(fill);
          score.append(label, track);
          score.title = option.text;
          result.append(score);
        }
        const descriptions = el('details', 'queue-descriptions');
        descriptions.append(el('summary', '', 'Destination definitions'));
        for (const option of sample.options) {
          const block = el('div');
          block.append(el('strong', '', option.label), el('p', '', option.text));
          descriptions.append(block);
        }
        result.append(descriptions);
      }
    }
    suggestion.append(result);
    updateResult();
    updateRoute();
    if (focusId) {
      const replacement = Array.from(detail.querySelectorAll<HTMLElement>('[id]'))
        .find(node => node.id === focusId);
      if (replacement && !replacement.hasAttribute('disabled')) replacement.focus({ preventScroll: true });
    }
    destinationSelect.addEventListener('change', () => {
      record.destination = destinationSelect.value;
      record.routed = false;
      updateRoute();
      renderList();
      notify();
    });
    editor.addEventListener('input', () => {
      record.revision += 1;
      record.request = ++serial;
      record.sample = {
        ...record.sample,
        id: `${mountId}:${record.originalId}:revision-${record.revision}`,
        state: editor.value,
      };
      record.prediction = undefined;
      record.error = '';
      record.pending = false;
      record.routed = false;
      result.setAttribute('aria-busy', 'false');
      suggestButton.setAttribute('aria-disabled', 'false');
      suggestButton.textContent = 'Suggest destination';
      updateResult();
      updateRoute();
      renderList();
      notify();
    });
  }

  async function predict(record: RecordState) {
    const request = ++serial;
    record.request = request;
    record.pending = true;
    record.error = '';
    record.prediction = undefined;
    const snapshot = clone(record.sample);
    if (selected === record) renderDetail();
    renderList();
    notify();
    try {
      const result = await config.predict(snapshot);
      if (disposed || record.request !== request || record.sample.id !== snapshot.id) return;
      const ids = new Set(snapshot.options.map(option => option.id));
      const seen = new Set<string>();
      const scores = result?.probabilities;
      if (!Array.isArray(scores) || scores.length !== ids.size || !scores.length ||
          scores.some(score => {
            if (!score || !ids.has(score.option_id) || seen.has(score.option_id) ||
                !Number.isFinite(score.probability) || score.probability < 0 || score.probability > 1) return true;
            seen.add(score.option_id);
            return false;
          }) ||
          Math.abs(scores.reduce((sum, score) => sum + score.probability, 0) - 1) > 0.000001) {
        throw new Error('The model returned an invalid score set. Try again or select a destination manually.');
      }
      record.prediction = { probabilities: scores.map(score => ({ ...score })) };
      live.textContent = 'Model suggestion available. Choose a destination to route this request.';
    } catch (error) {
      if (disposed || record.request !== request || record.sample.id !== snapshot.id) return;
      record.error = error instanceof Error ? error.message : 'Could not get a suggestion. Try again or select a destination manually.';
      live.textContent = 'Suggestion unavailable.';
    } finally {
      if (!disposed && record.request === request && record.sample.id === snapshot.id) {
        record.pending = false;
        renderList();
        if (selected === record) renderDetail();
        notify();
      }
    }
  }

  search.addEventListener('input', () => { query = search.value; renderList(); });
  filterSelect.addEventListener('change', () => { filter = filterSelect.value; renderList(); });
  renderList();
  renderDetail();
  return {
    dispose() {
      disposed = true;
      for (const record of records) record.request = ++serial;
      shell.remove();
    },
  };
}
