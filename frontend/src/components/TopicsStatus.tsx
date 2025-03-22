import { For, createResource,createEffect } from "solid-js";

import getTopics  from "../context/storageContext";

import styles from '../css/App.module.css';
import Plus from 'lucide-solid/icons/plus';

const { setTopics,topicNameSignal,setTopicName } = getTopics()!;

async function fetchUser(){
  const response = await fetch("/API/topics");
  const topics = await response.json();

  const topicsKeys: string[] = Object.keys(topics);

  const processedTopics = topicsKeys.map(key => {
    return [key, topics[key]];
  });

  return processedTopics;
}
const [topicsElements,{refetch}] = createResource(fetchUser);
createEffect(() => {
  topicNameSignal();
  console.log("Reloading topics");
  refetch()
})

async function click(topicName: string){
  console.log(`Clicked topic: ${topicName}`);

  const response = await fetch(`/API/topics/${topicName}`);
  
  let topicInfo = await response.json();

  topicInfo["name"]=topicName;

  console.log("Topic info: "+topicInfo);
  
  setTopics(topicInfo);

  setTopicName(topicName);
  
};

async function clickAddButton(){
  let index=1,topicName="";
  
  while(true){
    topicName="topic "+index
    if(topicsElements()!.findIndex(item => item[0] === topicName) === -1){
      console.log(`Adding topic: ${topicName}`);
      console.log(topicsElements());
      break;
    }
    index++;
  }

  const response = await fetch(`/API/topics/add?name=${topicName}`, {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  });
  
  await refetch();
  
  await click(topicName);
};

export default function TopicsStatus() {
  return (
    <>
      <For each={topicsElements()}>
        {(topic) => (
          <button class={styles.noDefaultButton} type="button" 
          onClick={() => click(topic[0])}>
            <div 
            classList={{[styles.status]: true,[styles.online]: topic[1], [styles.offline]: !topic[1]}}>
              {topic[0]}
            </div>
          </button>
        )}
      </For>
      <button class={styles.noDefaultButton} type="button"
      onClick={async() => clickAddButton()}>
        <div class={styles.plusButton}><Plus/></div>
      </button>
    </>
  );
}
