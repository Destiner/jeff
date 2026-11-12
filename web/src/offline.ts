export type OfflineStatus = {
  state: 'unsupported' | 'empty' | 'preparing' | 'ready' | 'error';
  message: string;
  loadedBytes?: number;
  totalBytes?: number;
  completedAssets?: number;
  totalAssets?: number;
  version?: string;
};

const protocol = 'jeff-offline-v1';
let registration: Promise<ServiceWorkerRegistration> | undefined;
const supported = () => typeof navigator !== 'undefined' && 'serviceWorker' in navigator && window.isSecureContext;
const unsupported = (): OfflineStatus => ({ state: 'unsupported', message: 'Offline storage requires a supported browser on localhost or HTTPS.' });
const errorStatus = (error: unknown): OfflineStatus => ({ state: 'error',
  message: `Offline storage: ${error instanceof Error ? error.message : String(error)}` });

function bounded<T>(promise: Promise<T>, milliseconds: number, message: string): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(message)), milliseconds);
    promise.then(value => { clearTimeout(timer); resolve(value); }, error => { clearTimeout(timer); reject(error); });
  });
}

async function controller(): Promise<ServiceWorker> {
  if (!registration) {
    registration = bounded((async () => {
      const existing = await navigator.serviceWorker.getRegistration('/');
      const options: RegistrationOptions = { scope: '/', updateViaCache: 'none' };
      const scriptUrl = new URL('/sw.js', location.origin).href;
      if (existing?.active?.scriptURL === scriptUrl && navigator.serviceWorker.controller?.scriptURL === scriptUrl) {
        // Offline reload must not wait for a network update check to fail.
        void bounded(navigator.serviceWorker.register('/sw.js', options), 30_000, 'Update check timed out.').catch(() => {});
        return existing;
      }
      return navigator.serviceWorker.register('/sw.js', options);
    })(), 30_000, 'Service worker registration timed out.').catch(error => { registration = undefined; throw error; });
  }
  await registration;
  await bounded(navigator.serviceWorker.ready, 30_000, 'Service worker activation timed out. Close other app tabs and reload to finish an update.');
  if (navigator.serviceWorker.controller) return navigator.serviceWorker.controller;
  return new Promise((resolve, reject) => {
    const finish = () => {
      const worker = navigator.serviceWorker.controller;
      if (worker) { cleanup(); resolve(worker); }
    };
    const cleanup = () => {
      clearTimeout(timer);
      navigator.serviceWorker.removeEventListener('controllerchange', finish);
    };
    const timer = setTimeout(() => { cleanup(); reject(new Error('Service worker did not take control. Reload this page.')); }, 30_000);
    navigator.serviceWorker.addEventListener('controllerchange', finish);
    finish();
  });
}

async function request(command: 'status' | 'prepare', onStatus?: (status: OfflineStatus) => void): Promise<OfflineStatus> {
  const activeWorker = await controller();
  const reg = await registration;
  const updating = command === 'prepare' && !!reg?.waiting;
  const worker = updating ? reg!.waiting! : activeWorker;
  const id = crypto.randomUUID();
  return new Promise((resolve, reject) => {
    const channel = new MessageChannel();
    const cleanup = () => {
      clearTimeout(timer);
      channel.port1.close();
      navigator.serviceWorker.removeEventListener('controllerchange', changed);
    };
    const cancel = () => {
      try { worker.postMessage({ protocol, command: 'cancel', id }); } catch { /* Worker may have stopped. */ }
    };
    const changed = () => {
      cancel(); cleanup(); reject(new Error('Offline worker changed. Reload before preparing again.'));
    };
    const timer = setTimeout(() => {
      cancel(); cleanup(); reject(new Error('Offline request timed out. Preparation was cancelled; check status before retrying.'));
    }, command === 'prepare' ? 16 * 60 * 1000 : 30_000);
    navigator.serviceWorker.addEventListener('controllerchange', changed);
    channel.port1.onmessage = event => {
      const reply = event.data;
      if (reply?.protocol !== protocol || reply.id !== id || !reply.status ||
          !['unsupported', 'empty', 'preparing', 'ready', 'error'].includes(reply.status.state) ||
          typeof reply.status.message !== 'string') return;
      let value: OfflineStatus = reply.status;
      if (updating && reply.done && value.state === 'ready') {
        cleanup();
        void request('status').then(current => {
          const final = { ...current, message: `${current.message} The update is saved; close all app tabs and reopen to activate it.` };
          try { onStatus?.(final); } catch { /* Status is still returned below. */ }
          resolve(final);
        }, reject);
        return;
      }
      if (reg?.waiting) value = { ...value, message: `${value.message} An update is waiting; prepare it before closing all app tabs to activate.` };
      // UI callbacks cannot interrupt the protocol or leave its timeout alive.
      try { onStatus?.(value); } catch (error) { console.error('Offline status callback failed', error); }
      if (reply.done) { cleanup(); resolve(value); }
    };
    channel.port1.onmessageerror = () => { cancel(); cleanup(); reject(new Error('Could not read the offline worker response.')); };
    try { worker.postMessage({ protocol, command, id, appUrl: import.meta.url, updating }, [channel.port2]); }
    catch (error) { cleanup(); reject(error); }
  });
}

export async function initializeOffline(onStatus: (s: OfflineStatus) => void): Promise<void> {
  if (!supported()) { onStatus(unsupported()); return; }
  try { await request('status', onStatus); }
  catch (error) { onStatus(errorStatus(error)); }
}

export async function prepareOffline(onStatus: (s: OfflineStatus) => void): Promise<void> {
  if (!supported()) { onStatus(unsupported()); return; }
  try { await request('prepare', onStatus); }
  catch (error) { onStatus(errorStatus(error)); }
}

export async function readOfflineStatus(): Promise<OfflineStatus> {
  if (!supported()) return unsupported();
  try { return await request('status'); }
  catch (error) { return errorStatus(error); }
}
