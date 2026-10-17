import { createContext, useCallback, useContext, useState } from 'react'

const Ctx = createContext(null)
export const useAssistant = () => useContext(Ctx)

export function AssistantProvider({ children }) {
  const [isOpen, setOpen] = useState(false)
  const [request, setRequest] = useState(null)
  // open({listen:true}) starts the microphone, open({product, explain:true}) explains a product, open({product}) asks about it,
  // open({prompt:'...'}) sends a message.
  const open = useCallback((opts = {}) => { setOpen(true); setRequest({ id: Date.now() + Math.random(), ...opts }) }, [])
  const close = useCallback(() => setOpen(false), [])
  return <Ctx.Provider value={{ isOpen, open, close, request }}>{children}</Ctx.Provider>
}
