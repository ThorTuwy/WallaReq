import getConfig, { type generalConfig,type ntfyConfig,type configType}  from "../context/configsStore";
import useTopics, { type Topics,type query } from "../context/storageContext";
import { createContext, useContext, createSignal, type Accessor, type Setter } from "solid-js";
import { For, createResource,createEffect } from "solid-js";


import styles from '../css/App.module.css';

import Power from 'lucide-solid/icons/power';
import Bolt from 'lucide-solid/icons/bolt';



export default function headderButtons() {
  const { setTopicName } = useTopics()!;
  const { config, setConfig } = getConfig()!;  
  
  const startSwichFetch = async () => {
    const response = await fetch("http://127.0.0.1:8000/status");
    const active = await response.text();

    return active=="true"
  };
  
    
  
  const [switchStatus,{refetch}] = createResource(startSwichFetch);


  const clickConfig = async () => {

    console.log(`Clicked in config`);

	  const response = await fetch(`http://127.0.0.1:8000/config`);
    
    let topicInfo:configType = await response.json();

    setConfig(topicInfo)
    setTopicName("CONFIG")
  };

  const clickStartSwich = async () => {

    console.log(`Swich toogle`);

	  if (switchStatus()){
      await fetch(`http://127.0.0.1:8000/stop`)
    }
    else{
      await fetch(`http://127.0.0.1:8000/start`)
    }
    refetch()
  };

  return(
    <>
    
    <div class={styles.headerButtons}>
        <button 
        class={[styles.actionButton, styles.config, styles.iconButton].join(" ")} type="button" onclick={() => clickConfig()}>
          <Bolt/>
        </button>
      </div>
      
      <div class={styles.headerButtons}>
        <button 
        classList={{[styles.iconButton]:true,[styles.actionButton]:true,[styles.add]:switchStatus(),[styles.remove]:!switchStatus()}}
        onclick={async () => clickStartSwich() }
        type="button">
          <Power/>
        </button>
    </div>
    </>
  )
}