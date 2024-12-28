import { For,createEffect, createResource, type JSX, Index } from "solid-js";

import useTopics, { type Topics,type query } from "../context/storageContext";
import getConfig, { type generalConfig,type ntfyConfig,type configType}  from "../context/configsStore";

import { type Accessor, type Setter } from "solid-js";
import { type SetStoreFunction,produce } from "solid-js/store"

import TextInput from '../components/forms/TextInput';

import styles from '../css/App.module.css';

import Trash from 'lucide-solid/icons/trash';
import Plus from 'lucide-solid/icons/plus';

//<p>{topics["enabled"].toString()}</p>


//<input type="text" id="keywords" name="keywords" value={topics["querys"][0]["keywords"]}></input><br></br>





function parseValue(value:any){
  if(value == undefined){
    return "";
  }
  return value;
}

async function saveChanges(){
  
  
}

export default function TopicInfo(props: any) {
    
    const { topics, setTopics,topicNameSignal,setTopicName } = useTopics()!;
    const { config, setConfig } = getConfig()!;  

    

    const handleInput = (currentTarget:HTMLInputElement|HTMLSelectElement,configName:keyof configType) => {
        console.log("pre:")
        console.log(config)
        const elementId = currentTarget.id ;

        let changeData:string|boolean=currentTarget.value;

        if(currentTarget.type==="checkbox"){
            changeData=(currentTarget as HTMLInputElement).checked;
        }
        
        setConfig(
            produce((config:configType) => {
                console.log(config);
                (config[configName] as any)[elementId] = changeData;
            })
        )

        console.log(config)
    };

    const saveChanges = async() => {

        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        };

        await fetch('http://localhost:8000/config', requestOptions)
        .then(response => response.json())
        .then(data => console.log(data));
        

        setTopicName("")
        setTopicName("CONFIG")
    };

    return (  
        <>      
            <h1>General</h1>
            <label for="sleepTime">Sleep time (s):</label>
            <TextInput id="sleepTime" topicName="general" onInput={handleInput} value={config["general"]["sleepTime"]} typeData="number" required={true}/>
            <h1>Notification methods</h1>
            <h2>NTFY</h2>

            <label for="token">Token:</label>
            <TextInput id="token" topicName="ntfy" onInput={handleInput} value={config["ntfy"]["token"]} typeData="text" required={true}/>

            <label for="domain">Domain:</label>
            <TextInput id="domain" topicName="ntfy"  onInput={handleInput} value={config["ntfy"]["domain"]} typeData="text" required={true}/>


            <button type="button" onclick={async() => await saveChanges()}>
                <div>Save Changes</div>
            </button>
        </>
    );
}
