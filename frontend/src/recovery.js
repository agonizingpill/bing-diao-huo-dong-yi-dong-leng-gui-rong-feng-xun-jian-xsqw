import {awaitCompute, openComputes} from './api.js';
import {el, display} from './dom.js';
import {COMPUTE_STATES, evidence} from './store.js';
import {status} from './widgets.js';

const LABEL = {queued: '排队中', running: '计算中', ready: '已出分', rejected: '计算被拒绝'};

export function fillToken(token) {
  const form = document.getElementById('record_seam');
  if (!form) return false;
  form.elements.token.value = token;
  evidence.save(token);
  form.elements.token.focus();
  return true;
}

export function recoveryBoard(role, refresh) {
  const notice = status('');
  const board = el('section', {class:'recovery', 'aria-label':'未办完的融缝计算'},
    el('h3', {}, '未办完的融缝计算'),
    el('p', {class:'hint'}, '换班或重启后可在此取回原样本的计算；已出分的直接接着签认。'),
    el('div', {class:'records stack'}, status('正在读取…')),
    notice);
  const list = board.querySelector('.records');

  const card = row => {
    const rejected = row.status === 'rejected';
    const pending = row.status !== 'ready' && !rejected;
    const action = rejected
      ? status(row.detail || '计算被拒绝，请核对样本后重算', 'error')
      : role === 'reviewer'
        ? el('button', {type:'button'}, pending ? '跟进计算' : '取回并签认')
        : status(pending ? '等待计算完成后由复核员签认' : '已出分，等待复核员签认');

    if (role === 'reviewer' && !rejected) action.addEventListener('click', async () => {
      action.disabled = true;
      notice.className = 'status';
      try {
        if (pending) {
          const data = await awaitCompute(row.token, current => {
            notice.textContent = `${display(row.sample)} · ${LABEL[current.status] || COMPUTE_STATES[current.status] || current.status}`;
          });
          if (data.status === 'rejected') throw new Error(data.detail);
        }
        if (!fillToken(row.token)) throw new Error('请切换到复核员签认表单');
        notice.textContent = `已带入凭据 ${row.token}，核对后提交签认。`;
        notice.classList.add('ok');
        await refresh();
      } catch (error) {
        notice.textContent = error.message;
        notice.classList.add('error');
      } finally { action.disabled = false; }
    });

    return el('article', {class:'record'},
      el('h3', {}, display(row.sample) + ' · ' + (LABEL[row.status] || row.status)),
      el('dl', {}, el('dt', {}, '计算凭据'), el('dd', {}, row.token),
        el('dt', {}, '局部相对密度'), el('dd', {}, row.result ? display(row.result.density) : '—'),
        el('dt', {}, '基线门槛'), el('dd', {}, row.result ? display(row.result.threshold) : '—')),
      action);
  };

  const render = rows => {
    list.replaceChildren(...(rows.length
      ? rows.map(card)
      : [status('没有待签认的计算。')]));
  };

  board.load = async () => {
    try { render(await openComputes()); }
    catch (error) { list.replaceChildren(status(error.message, 'error')); }
  };
  if (role !== 'reviewer') {
    board.querySelector('.hint').textContent = '此处列出你提交但尚未签认的计算；已出分的可带回凭据。';
  }
  return board;
}
