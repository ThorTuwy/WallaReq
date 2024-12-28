import { For, createResource,createEffect, type Setter } from "solid-js";
import getTopics, { type Topics,type query}  from "../context/storageContext";

import styles from '../css/App.module.css';

import Plus from 'lucide-solid/icons/plus';

export default function TopicsStatus(props: any) {
  const { topics, setTopics,topicNameSignal,setTopicName } = getTopics()!;
  
  const fetchUser = async () => {
    const response = await fetch("http://127.0.0.1:8000/topics");
    const topics = await response.json();

    const topicsKeys: string[] = Object.keys(topics);

    const processedTopics = topicsKeys.map(key => {
      return [key, topics[key]];
    });

    return processedTopics;
  };

  

  const [topicsElements,{refetch}] = createResource(fetchUser);

  createEffect(() => {
    topicNameSignal();
    console.log("Reloading topics");
    refetch()
  })

  const click = async (topicName: string) => {
    console.log(`Clicked topic: ${topicName}`);

	  const response = await fetch(`http://127.0.0.1:8000/topics/${topicName}`);
    
    let topicInfo = await response.json();

    topicInfo["name"]=topicName;
  
    console.log("Topic info: "+topicInfo);
    setTopicName(topicName);
    setTopics(topicInfo)
  };

  const clickAddButton = async () => {
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

    const response = await fetch(`http://127.0.0.1:8000/topics/add?name=${topicName}`, {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    await refetch();
    
    await click(topicName);
  };
  
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
