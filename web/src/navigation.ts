import './navigation.css';
export function navigation(host: HTMLElement, current: 'queue' | 'chat' | 'playground'): HTMLSpanElement {
  const group = document.createElement('div'); group.className = 'app-navigation';
  const nav = document.createElement('nav'); nav.setAttribute('aria-label', 'Apps');
  for (const [id, name, href] of [['queue','Requests','/'],['chat','Messages','/chat.html'],['playground','Playground','/playground.html']]) {
    const link = document.createElement('a'); link.href = href; link.textContent = name;
    if (id === current) link.setAttribute('aria-current','page');
    nav.append(link);
  }
  const status = document.createElement('span'); status.className = 'app-model-status';
  status.setAttribute('role', 'status');
  group.append(nav, status); host.append(group); return status;
}
