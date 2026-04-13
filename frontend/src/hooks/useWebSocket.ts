'use client';

import { useEffect, useRef, useState, useCallback } from 'react';

export type WsStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

export interface UseWebSocketOptions {
  /** Called when a JSON message is received. */
  onMessage?: (data: unknown) => void;
  /** Called when the connection opens. */
  onOpen?: () => void;
  /** Called when the connection closes. */
  onClose?: () => void;
  /** Called on error. */
  onError?: (event: Event) => void;
  /** Reconnect after this many ms on disconnect (0 = no reconnect). Default 3000. */
  reconnectDelay?: number;
  /** Maximum reconnect attempts. Default 5. */
  maxReconnects?: number;
}

export interface UseWebSocketReturn {
  status: WsStatus;
  send: (data: unknown) => void;
  disconnect: () => void;
}

/**
 * React hook for managing a WebSocket connection.
 *
 * Automatically reconnects on disconnect (configurable), parses JSON messages,
 * and cleans up on unmount.
 *
 * @example
 * ```tsx
 * const { status, send } = useWebSocket('ws://localhost:8080/ws', {
 *   onMessage: (data) => console.log(data),
 * });
 * ```
 */
export function useWebSocket(url: string | null, options: UseWebSocketOptions = {}): UseWebSocketReturn {
  const {
    onMessage,
    onOpen,
    onClose,
    onError,
    reconnectDelay = 3_000,
    maxReconnects = 5,
  } = options;

  const [status, setStatus] = useState<WsStatus>('disconnected');
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectCount = useRef(0);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const intentionalClose = useRef(false);

  const connect = useCallback(() => {
    if (!url) return;

    setStatus('connecting');
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus('connected');
      reconnectCount.current = 0;
      onOpen?.();
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data as string);
        onMessage?.(data);
      } catch {
        onMessage?.(event.data);
      }
    };

    ws.onclose = () => {
      setStatus('disconnected');
      onClose?.();
      wsRef.current = null;

      if (!intentionalClose.current && reconnectDelay > 0 && reconnectCount.current < maxReconnects) {
        reconnectCount.current += 1;
        reconnectTimer.current = setTimeout(connect, reconnectDelay);
      }
    };

    ws.onerror = (event) => {
      setStatus('error');
      onError?.(event);
    };
  }, [url, onMessage, onOpen, onClose, onError, reconnectDelay, maxReconnects]);

  useEffect(() => {
    if (!url) return;
    intentionalClose.current = false;
    connect();

    return () => {
      intentionalClose.current = true;
      if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
      wsRef.current?.close();
    };
  }, [url, connect]);

  const send = useCallback((data: unknown) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(typeof data === 'string' ? data : JSON.stringify(data));
    }
  }, []);

  const disconnect = useCallback(() => {
    intentionalClose.current = true;
    if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
    wsRef.current?.close();
  }, []);

  return { status, send, disconnect };
}
