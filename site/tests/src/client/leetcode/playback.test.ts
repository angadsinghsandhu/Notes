import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { createPlayback } from '../../../../src/client/leetcode/playback.js';
import type { AlgorithmTrace } from '../../../../src/content/index.js';

const trace: AlgorithmTrace = {
  version: 1,
  problemId: 'leetcode:1',
  approachId: 'hash-map',
  exampleId: 'duplicate',
  implementationSha256: 'a'.repeat(64),
  result: [0, 1],
  frames: [
    {
      stepId: 'lookup-0',
      codeLines: [1],
      explanation: 'The map is empty.',
      state: { kind: 'table', columns: ['Value', 'Index'], rows: [] },
      highlights: [],
    },
    {
      stepId: 'record-0',
      codeLines: [2],
      explanation: 'Record value 3 at index 0.',
      state: { kind: 'table', columns: ['Value', 'Index'], rows: [[3, 0]] },
      highlights: [{ row: 0, column: 0 }],
    },
    {
      stepId: 'lookup-1',
      codeLines: [1],
      explanation: 'There is no complement for value 3.',
      state: { kind: 'table', columns: ['Value', 'Index'], rows: [[3, 0]] },
      highlights: [],
    },
    {
      stepId: 'record-1',
      codeLines: [2],
      explanation: 'The latest occurrence of 3 is now index 1.',
      state: { kind: 'table', columns: ['Value', 'Index'], rows: [[3, 1]] },
      highlights: [{ row: 0, column: 0 }],
    },
  ],
};

beforeEach(() => vi.useFakeTimers());
afterEach(() => vi.useRealTimers());

test('backtracking restores the full frame after a hash-table overwrite', () => {
  const player = createPlayback(trace);
  player.next();
  player.next();
  const priorFrame = player.getFrame();
  const expectedFrame = structuredClone(priorFrame);
  expect(expectedFrame).toMatchObject({
    stepId: 'lookup-1',
    state: { rows: [[3, 0]] },
    highlights: [],
  });

  player.next();
  expect(player.getFrame()).toMatchObject({
    stepId: 'record-1',
    state: { rows: [[3, 1]] },
    highlights: [{ row: 0, column: 0 }],
  });

  expect(priorFrame).toEqual(expectedFrame);
  player.previous();
  expect(player.getFrame()).toEqual(expectedFrame);
  expect(player.getState()).toEqual({
    index: 2,
    total: trace.frames.length,
    playing: false,
    speed: 1,
  });
});

test('starts paused and manual moves pause an active clock in either direction', () => {
  const player = createPlayback(trace);
  vi.advanceTimersByTime(5000);
  expect(player.getFrame()).toEqual(trace.frames[0]);
  expect(vi.getTimerCount()).toBe(0);

  player.play();
  player.next();
  expect(player.getFrame()).toEqual(trace.frames[1]);
  expect(player.getState().playing).toBe(false);
  expect(vi.getTimerCount()).toBe(0);

  player.play();
  player.previous();
  vi.advanceTimersByTime(5000);
  expect(player.getFrame()).toEqual(trace.frames[0]);
  expect(player.getState().playing).toBe(false);
  expect(vi.getTimerCount()).toBe(0);
});

test('reset cancels the pending tick and returns to the first frame at the selected speed', () => {
  const player = createPlayback(trace);
  player.next();
  player.setSpeed(2);
  player.play();
  vi.advanceTimersByTime(499);

  player.reset();
  vi.advanceTimersByTime(500);

  expect(player.getFrame()).toEqual(trace.frames[0]);
  expect(player.getState()).toMatchObject({
    index: 0,
    playing: false,
    speed: 2,
  });
  expect(vi.getTimerCount()).toBe(0);
});

test('repeated play keeps one clock and timed playback stops on the last frame', () => {
  const onChange = vi.fn();
  const player = createPlayback(trace, onChange);

  player.play();
  vi.advanceTimersByTime(500);
  player.play();
  expect(vi.getTimerCount()).toBe(1);
  vi.advanceTimersByTime(499);
  expect(player.getState().index).toBe(0);
  vi.advanceTimersByTime(1);
  expect(player.getState()).toMatchObject({ index: 1, playing: true });

  vi.advanceTimersByTime(1000 * (trace.frames.length - 2));
  expect(player.getFrame()).toEqual(trace.frames.at(-1));
  expect(player.getState()).toMatchObject({
    index: trace.frames.length - 1,
    playing: false,
  });
  expect(onChange).toHaveBeenCalledTimes(trace.frames.length);
  expect(onChange).toHaveBeenLastCalledWith(player.getState());
  expect(vi.getTimerCount()).toBe(0);

  player.play();
  player.next();
  expect(onChange).toHaveBeenCalledTimes(trace.frames.length);
  expect(vi.getTimerCount()).toBe(0);
});

test('a valid speed change replaces a pending tick and pause cancels it', () => {
  const onChange = vi.fn();
  const player = createPlayback(trace, onChange);

  player.play();
  vi.advanceTimersByTime(900);
  player.setSpeed(0.5);
  expect(onChange).toHaveBeenLastCalledWith({
    index: 0,
    total: trace.frames.length,
    playing: true,
    speed: 0.5,
  });
  expect(vi.getTimerCount()).toBe(1);
  vi.advanceTimersByTime(1999);
  expect(player.getFrame()).toEqual(trace.frames[0]);
  vi.advanceTimersByTime(1);
  expect(player.getFrame()).toEqual(trace.frames[1]);

  player.setSpeed(2);
  vi.advanceTimersByTime(499);
  player.pause();
  expect(vi.getTimerCount()).toBe(0);
  expect(onChange).toHaveBeenLastCalledWith(player.getState());
  expect(player.getState().playing).toBe(false);
  vi.advanceTimersByTime(5000);
  expect(player.getFrame()).toEqual(trace.frames[1]);
});

test('unsupported and unchanged speeds leave scheduling and notifications alone', () => {
  const onChange = vi.fn();
  const player = createPlayback(trace, onChange);
  player.play();
  vi.advanceTimersByTime(500);

  for (const speed of [1, NaN, Infinity, -1, 0, 10]) player.setSpeed(speed);

  expect(onChange).toHaveBeenCalledOnce();
  expect(player.getState().speed).toBe(1);
  vi.advanceTimersByTime(500);
  expect(player.getFrame()).toEqual(trace.frames[1]);
});

test('the first frame is the lower bound and a single frame stays paused', () => {
  const onChange = vi.fn();
  const player = createPlayback(trace, onChange);
  player.previous();
  expect(player.getFrame()).toEqual(trace.frames[0]);

  const single = createPlayback(
    { ...trace, frames: trace.frames.slice(0, 1) },
    onChange,
  );
  single.play();
  single.next();
  single.previous();
  single.reset();
  expect(single.getFrame()).toEqual(trace.frames[0]);
  expect(single.getState()).toEqual({
    index: 0,
    total: 1,
    playing: false,
    speed: 1,
  });
  expect(vi.getTimerCount()).toBe(0);
  expect(onChange).not.toHaveBeenCalled();
});

test('destroy clears the timer, detaches the observer and freezes the controller', () => {
  const onChange = vi.fn();
  const player = createPlayback(trace, onChange);
  player.next();
  player.play();
  expect(onChange).toHaveBeenCalledTimes(2);

  player.destroy();
  player.destroy();
  player.play();
  player.pause();
  player.previous();
  player.next();
  player.reset();
  player.setSpeed(2);
  vi.advanceTimersByTime(5000);

  expect(player.getFrame()).toEqual(trace.frames[1]);
  expect(player.getState()).toMatchObject({
    index: 1,
    playing: false,
    speed: 1,
  });
  expect(onChange).toHaveBeenCalledTimes(2);
  expect(vi.getTimerCount()).toBe(0);
});
