import { createResource } from "solid-js";

import getConfig, { type configType }  from "../context/configsStore";
import useTopics from "../context/storageContext";

import styles from '../css/App.module.css';
import Power from 'lucide-solid/icons/power';
import Bolt from 'lucide-solid/icons/bolt';

const { setTopicName } = useTopics()!;
const { setConfig } = getConfig()!;  

async function startSwichFetch(){
  const response = await fetch("/API/status");
  const active = await response.text();

  return active=="true"
}
const [switchStatus,{refetch}] = createResource(startSwichFetch);

async function clickConfig(){
  const response = await fetch(`/API/config`);
  
  let topicInfo:configType = await response.json();

  setConfig(topicInfo)
  setTopicName("CONFIG")
}

async function clickStartSwich(){
  let query = "/API/start" 
  //Because this is a switch, we stoop the app when the app is running
  if (switchStatus()){
    query=`/API/stop`
  }
  fetch(query)
  refetch()
}

export default function headderButtons() {
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