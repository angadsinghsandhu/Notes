import type { AlgorithmTrace, TraceFrame } from '../../content/index.js';

export const PLAYBACK_SPEEDS = [0.5, 1, 2] as const;

export interface PlaybackState {
  readonly index: number;
  readonly total: number;
  readonly playing: boolean;
  readonly speed: (typeof PLAYBACK_SPEEDS)[number];
}

export interface PlaybackController {
  getFrame(): TraceFrame;
  getState(): PlaybackState;
  next(): void;
  previous(): void;
  reset(): void;
  play(): void;
  pause(): void;
  setSpeed(rate: number): void;
  destroy(): void;
}

/** Create a paused controller for a validated trace with at least one frame. */
export function createPlayback(
  { frames }: AlgorithmTrace,
  onChange?: (state: PlaybackState) => void,
): PlaybackController {
  const last = frames.length - 1;
  let state: PlaybackState = {
    index: 0,
    total: frames.length,
    playing: false,
    speed: 1,
  };
  let timer: ReturnType<typeof setTimeout> | undefined;
  let destroyed = false;

  function cancelTick(): void {
    clearTimeout(timer);
    timer = undefined;
  }

  function update(index: number, playing: boolean, speed = state.speed): void {
    if (
      destroyed ||
      (index === state.index &&
        playing === state.playing &&
        speed === state.speed)
    )
      return;

    cancelTick();
    state = { index, total: state.total, playing, speed };
    if (playing) {
      timer = setTimeout(() => {
        const next = state.index + 1;
        update(next, next < last);
      }, 1000 / speed);
    }
    onChange?.(state);
  }

  return {
    getFrame: () => frames[state.index]!,
    getState: () => state,
    next: () => update(Math.min(last, state.index + 1), false),
    previous: () => update(Math.max(0, state.index - 1), false),
    reset: () => update(0, false),
    play: () => update(state.index, state.index < last),
    pause: () => update(state.index, false),
    setSpeed(rate) {
      const speed = PLAYBACK_SPEEDS.find((supported) => supported === rate);
      if (speed !== undefined) update(state.index, state.playing, speed);
    },
    destroy() {
      destroyed = true;
      cancelTick();
      onChange = undefined;
      state = { ...state, playing: false };
    },
  };
}
