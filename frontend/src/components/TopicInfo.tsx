import { For } from "solid-js";
import useTopics, { type Topics,type query } from "../context/storageContext";
import { type Accessor, type Setter } from "solid-js";
import { type SetStoreFunction,produce } from "solid-js/store"

import TextInput from '../components/forms/TextInput';

import styles from '../css/App.module.css';

import Trash from 'lucide-solid/icons/trash';
import Plus from 'lucide-solid/icons/plus';


function parseValue(value:any){
  if(value == undefined){
    return "";
  }
  return value;
}


function removeNtfyChannel(index: number, setTopics: SetStoreFunction<Topics>) {
  setTopics(
    produce((topics) => {
      topics.ntfy.splice(index, 1);
    })
  );
}

function newNtfyChannel(setTopics: SetStoreFunction<Topics>) {
  const newChannel=(document.getElementById("ntfyChannel_new")!as HTMLInputElement).value
  if(newChannel===""){
    return;
  }
  setTopics(
    produce((topics) => {
      topics.ntfy.push(newChannel);
    })
  );
  (document.getElementById("ntfyChannel_new")!as HTMLInputElement).value="";
}

function newQueryElement(topics:Topics,setTopics: SetStoreFunction<Topics>) {
  
  let index=1,queryKeywords="";
  while(true){
    queryKeywords="Query_"+index
    if(topics["querys"].findIndex(item => item["keywords"] === queryKeywords) === -1){
      break;
    }
    index++;
  }
  setTopics(
    "querys",
    produce((querys) => {
      querys.push({"keywords":queryKeywords} as query);
    })
  );
}

function removeQueryElement(queryName:string,topics:Topics,setTopics: SetStoreFunction<Topics>) {
  
  const indice = topics["querys"].findIndex(item => item["keywords"] === queryName);
  setTopics(
    "querys",
    produce((querys) => {
      querys.splice(indice, 1);
    })
  );
}




async function saveChanges(topics:Topics,topicNameSignal:Accessor<string>,setTopicName:Setter<string>){
  
  
  const topicRealName=topicNameSignal();

  if(topics["name"]!=topicRealName){
    const response = await fetch("/API/topics");
    const topicsNames: string[] = Object.keys(await response.json());
    console.log(topicsNames);
    console.log("topicsname: "+topics["name"])
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
    .then(response => response.json())
    .then(data => console.log(data));
  
  if(topics["name"]!=topicRealName){
    const response = await fetch(`/API/topics/remove?name=${topicRealName}`, {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
  }

  setTopicName("")
  setTopicName(topics["name"])
  
}

export default function TopicInfo(props: any) {
  
  const { topics, setTopics,topicNameSignal,setTopicName } = useTopics()!;

  const handleInput = (currentTarget:HTMLInputElement|HTMLSelectElement,topicName:false|string) => {
   
    const elementId = currentTarget.id;

    let changeData:string|boolean=currentTarget.value;

    if(currentTarget.type==="checkbox"){
      changeData=(currentTarget as HTMLInputElement).checked;
    }

    console.log("changeData: "+currentTarget);



    //No uppercase for name
    if(elementId==="name"){
      changeData=(changeData as string).toLowerCase();
    }
    
    if(topicName === false){
      setTopics(elementId as keyof Topics,changeData);
      return;
    }

    //Special checks for the keywords
    if(elementId==="keywords"){
      if(changeData===""){
        throw new Error("Keywords can't be empty");
      }
      if(topics["querys"].findIndex(item => item["keywords"] === changeData)!=-1 ){
        throw new Error("There is already a query with the same keywords");
      }
    }

    const indice = topics["querys"].findIndex(item => item["keywords"] === topicName);

    if(indice == -1){
      throw new Error("There is no element with the name: "+topicName);
    }


    setTopics("querys",indice,elementId as keyof query,changeData);
  };

  const deleteTopic = async () => {
    const userResponse = confirm("Are you sure you want to delete this topic?");
    
    if(!userResponse){
      return;
    }
    
    const response = await fetch(`/API/topics/remove?name=${topicNameSignal()}`, {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });

    setTopicName("")
  }
  
  return (  
    <>

      
      
      
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
      <TextInput id="name" topicName={false} onInput={handleInput} value={topics["name"]} typeData="text" required={true}/>
      <br/>


      <label for="Running">Running: </label>
      <TextInput id="enabled" topicName={false} onInput={handleInput} value={topics["enabled"]} typeData="checkbox"/>
      



      <h1>Queries</h1>  
      <For each={topics["querys"]}>
        {(query) => (
          <>
            <br/>
            <div style={{display: "flex","justify-content": "space-between"}}>
                <h2  class={styles["inline-header"]}>{query["keywords"]}</h2>
                <button  class={[styles.actionButton, styles.remove, styles.iconButton, styles.ButtonTitle].join(" ")} type="button" onclick={() => removeQueryElement(query["keywords"],topics, setTopics)}>
                  <Trash/>
                </button>
            </div>
            <br/>
            
            <label for="keywords">Keywords: </label>
            <TextInput id="keywords" topicName={query["keywords"]} onInput={handleInput} value={query["keywords"]} typeData="text"/>
            <br/>

            <label for="order_by">Order by: </label>
            <select required name="order_by" id="order_by" 
            value={parseValue(query["order_by"])}
            onInput={(event) => handleInput(event.currentTarget, query["keywords"])}>
              <option value="most_relevance">most_relevance</option>
              <option value="newest">newest</option>
              <option value="price_low_to_high">price_low_to_high</option>
              <option value="price_high_to_low">price_high_to_low</option>
              <option value="newest">closest</option>
            </select>
            
            

            <label for="max_sale_price">Max sale price: </label>
            <TextInput id="max_sale_price" topicName={query["keywords"]} onInput={handleInput} value={query["max_sale_price"]} typeData="number"/>
            <br/>

            <label for="min_sale_price">Min sale price: </label>
            <TextInput id="min_sale_price" topicName={query["keywords"]} onInput={handleInput} value={query["min_sale_price"]} typeData="number"/>
            <br/>

            <label for="category_ids">Category IDs: </label>
            <TextInput id="category_ids" topicName={query["keywords"]} onInput={handleInput} value={query["category_ids"]} typeData="number"/>

            <label for="latitude">Latitude: </label>
            <TextInput id="latitude" topicName={query["keywords"]} onInput={handleInput} value={query["latitude"]} typeData="number"/>
            <br/>

            <label for="longitude">Longitude: </label>
            <TextInput id="longitude" topicName={query["keywords"]} onInput={handleInput} value={query["longitude"]} typeData="number"/>
            <br/>

            <label for="condition">Condition: </label>
            <select name="condition" id="condition" 
            value={parseValue(query["condition"])}
            onInput={(event) => handleInput(event.currentTarget, query["keywords"])}>
              <option value=""></option>
              <option value="new">new</option>
              <option value="as_good_as_new">as_good_as_new</option>
              <option value="good">good</option>
              <option value="fair">fair</option>
              <option value="has_given_it_all">has_given_it_all</option>
            </select><br/><br/>


            <label for="is_shippable">Only products with shipping: </label>
            <TextInput id="is_shippable" topicName={query["keywords"]} onInput={handleInput} value={query["is_shippable"]} typeData="checkbox"/>
            <br/><br/>
          </>
        )}
      </For>
      <div style={{display: "flex","justify-content": "center"}}>
        <button class={styles.noDefaultButton} type="button" onclick={() => newQueryElement(topics,setTopics)}>
          <div class={styles.plusButton}>
            <Plus/>
          </div>
        </button>
        <div>
      </div>
        
      </div>

      <div>
        <h1>Notificacions Methods</h1>  
        <h2>NTFY</h2>
        <label for="Channels">Channels: </label><br/>
        <For each={topics["ntfy"]}>
          {(channel,index) => (
            <>
              <div style={{display: "flex"}}>
                <input disabled required type="text" id={"ntfyChannel_"+index()} name="channels"
                value={channel}>
                  <p>sis</p>
                </input>
                <button class={[styles.actionButton, styles.remove, styles.iconButton].join(" ")} type="button" onclick={() => removeNtfyChannel(index(), setTopics)}>
                  <Trash/>
                </button>
              </div>
            </>
          )}
        </For>
        <br></br>
      
        
        <div style={{display: "flex"}}>
          <input type="text" id="ntfyChannel_new" name="channels"></input>
          <button class={[styles.actionButton, styles.add, styles.iconButton].join(" ")} type="button" onclick={() => newNtfyChannel(setTopics)}>
            <Plus/>
          </button>
        </div>


      </div>
      <br/><br/>
      <button type="button" onclick={async() => await saveChanges(topics,topicNameSignal,setTopicName)}>
        <div>Save Changes</div>
      </button>

      

    </>
  );
}
