import { For } from "solid-js";
import { produce } from "solid-js/store"

import useTopics from "../context/storageContext";
import TextInput from './forms/InputObjects';

import styles from '../css/App.module.css';
import Trash from 'lucide-solid/icons/trash';
import Plus from 'lucide-solid/icons/plus';

import { formToApiJson } from "../utils/formDataPaser";

import { TopicsToCheck } from "../auto-generated-types/topicsToCheck"

import template_topics from "../templates/template_topicsToCheck.json";

const { topics, setTopics,topicNameSignal,setTopicName } = useTopics()!;

function newQueryElement() {
  let index=1,queryKeywords="";
  while(true){
    queryKeywords="Query_"+index
    if(topics["querys"]==null || topics["querys"].findIndex(item => item["keywords"] === queryKeywords) === -1){
      break;
    }
    index++;
  }
  setTopics(
    "querys",
    produce((querys) => {
      querys?.push({"keywords":queryKeywords});
    })
  );
}

function removeQueryElement(queryName:string|undefined) {
  if(queryName==null){
    console.error('Query not found');
    return null
  }
  const indice = topics["querys"]?.findIndex(item => item["keywords"] === queryName);
  if(!indice) {
    console.error('Query not found');
     return null
  }
  setTopics(
    "querys",
    produce((querys) => {
      querys?.splice(indice, 1);
    })
  );
}

function handleInput(currentTarget:HTMLInputElement|HTMLSelectElement,topicName:false|string){
   
}

//This is used, for the name changing in h2 reactive to the input
function handleInputName(currentTarget:HTMLInputElement|HTMLSelectElement,topicName:false|string){
  const elementId = currentTarget.id;

  let changeData:string=currentTarget.value;

  setTopics(elementId as keyof TopicsToCheck,changeData);
}

async function deleteTopic(){

  if(!confirm("Are you sure you want to delete this topic?")){
    return;
  }
  
  await fetch(`/API/topics/remove?name=${topicNameSignal()}`, {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  });

  setTopicName("")
}

async function onSubmit(e: SubmitEvent){
  e.preventDefault();
  const form = e.currentTarget as HTMLFormElement;
  
  let topics = formToApiJson(form);

  const topicRealName=topicNameSignal();

  if(topics["name"]!=topicRealName){
    const response = await fetch("/API/topics");
    const topicsNames: string[] = Object.keys(await response.json());

    if( topicsNames.includes(  topics["name"] ) ){
      throw new Error("There is already a topic with the name: "+topics["name"]);
    }
  }

  const requestOptions = {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(topics)
  };

  await fetch('/API/topics/update', requestOptions)
  
  if(topics["name"]!=topicRealName){
    await fetch(`/API/topics/remove?name=${topicRealName}`, {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
  }

  setTopics(topics)

  //This is done to force a reload of the Heeadders buttons
  setTopicName("")
  setTopicName(topics["name"])
}

export default function TopicInfo() {
  const enabled=template_topics["enabled"];
  
  return (  
    <>
      <form onSubmit={onSubmit}>
      <div class={styles.titleContainer}>
        <h1>{topics["name"]}</h1>
        
        <button 
        class={[styles.actionButton, styles.remove, styles.iconButton, styles.ButtonTitle].join(" ")}
        type="button"
        onclick={async() => await deleteTopic()}>
            <Trash/>
        </button>
      </div>
      
       

      <label for="Name">Name: </label>
      <TextInput id="name" topicName={false} onInput={handleInputName} value={topics.name} typeData="text" required={true}/>
      <br/>

      
      {/* FIX: When Running value is modified but not save, when you change topic, you are going to see the same value as before,
       because of reactivty dosent consider de fact that checkbox dont change any propierty when cliked*/}
      
      <label for="Running">Running: </label>
      <TextInput id="enabled" topicName={false} onInput={handleInput} value={topics.enabled} typeData="checkbox"/>
      <br/>

      <h1>Queries</h1>  

      <For each={topics["querys"]}>
        {(query,index) => {
          console.log(topics["name"]);
          return (
            <>
              <br/>
              <div style={{display: "flex","justify-content": "space-between"}}>
                  <h2  class={styles["inline-header"]}>{query["keywords"]}</h2>
                  <button  class={[styles.actionButton, styles.remove, styles.iconButton, styles.ButtonTitle].join(" ")} type="button" 
                  onclick={() => removeQueryElement(query["keywords"])}>
                    <Trash/>
                  </button>
              </div>
              <For each={Object.keys(template_topics["querys"])}>
                {(key) => {
                    if (key==="type") return;
                    
                    const keyTemplate=template_topics["querys"][key as keyof typeof template_topics["querys"]];
                    const id=`querys.${index()}.${key}`;
                    return (
                      <>
                          <label for={id}>{keyTemplate["textLabel" as keyof typeof keyTemplate]}</label>
                          <TextInput id={id} topicName={query["keywords"]} onInput={handleInput} value={(query as any)[key]} 
                          typeData={keyTemplate["type" as keyof typeof keyTemplate]} required={keyTemplate["required" as keyof typeof keyTemplate]} options={keyTemplate["options" as keyof typeof keyTemplate]}/>
                      </>
                    )
                }}
              </For>
            </>
          )
        }}
      </For>
      
      <div style={{display: "flex","justify-content": "center"}}>
        <button class={styles.noDefaultButton} type="button" onclick={() => newQueryElement()}>
          <div class={styles.plusButton}>
            <Plus/>
          </div>
        </button>
        <div>
      </div>
        
      </div>


      <h1>Notificacions Methods</h1>  

      <For each={Object.keys(template_topics["notifications"])}>
        {(notification) => {
          const notificationTemplate=template_topics["notifications"][notification as keyof typeof template_topics["notifications"]];
          return (
            <>
              <h2>{notification}</h2>
              <For each={Object.keys(notificationTemplate)}>
                {(key) => {
                    const keyTemplate=notificationTemplate[key as keyof typeof notificationTemplate];
                    const id=`notifications.${notification}.${key}`;
                    return (
                      <>
                          <label for={id}>{keyTemplate["textLabel"]}</label>
                          <TextInput id={id} topicName={""} onInput={handleInput} value={(topics as any)["notifications"]!=undefined ? (topics as any)["notifications"][notification][key] : []} 
                          typeData={keyTemplate["type"]} required={keyTemplate["required"]} options={keyTemplate["options"]}/>
                      </>
                    )
                }}
              </For>
            </>
          )
        }}
      </For>

      <br/>
        
      <button type="submit">Submit</button>
      </form>

    </>
  );
}
