import { createStore } from "solid-js/store"



const [config, setConfig] = createStore({} as any);




export default function getConfig() {
  return {config,setConfig};
}
