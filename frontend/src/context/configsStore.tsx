import { createContext, useContext, createSignal, type Accessor, type Setter } from "solid-js";
import { createStore,type SetStoreFunction } from "solid-js/store"


export type generalConfig = {
    sleepTime: number
}

export type ntfyConfig = {
    token: number,
    domain: string,
}


export type configType = {
    general: generalConfig,
    ntfy: ntfyConfig
}

const [config, setConfig] = createStore({} as configType);

export default function getConfig() {
  return { config, setConfig };
}
