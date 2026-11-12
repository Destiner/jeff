import './demos.css';
import { mountChat } from './apps/chat';
import { sentimentExamples } from './examples';
import { navigation } from './navigation';
import { createSession } from './session';
const root = document.querySelector<HTMLElement>('#app')!;
let session: ReturnType<typeof createSession>;
mountChat(root, { samples: sentimentExamples, question: sentimentExamples[0].question,
  options: sentimentExamples[0].options, predict: sample => session.predict(sample) });
const status = navigation(root.querySelector<HTMLElement>('.chat-header')!, 'chat');
session = createSession(status);
window.addEventListener('pagehide', () => { void session.dispose(); });
window.addEventListener('pageshow', event => { if (event.persisted) session = createSession(status); });
