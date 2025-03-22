import getConfig  from "../context/configsStore";
import TextInput from './forms/InputObjects';
import { formToApiJson } from "../utils/formDataPaser";
import { For } from "solid-js";

import configTemplate from "../templates/template_configs.json";

const { config } = getConfig()!;  



function handleInput(currentTarget:HTMLInputElement|HTMLSelectElement,configName:any){

}


async function onSubmit(e: SubmitEvent){
    e.preventDefault();
    const form = e.currentTarget as HTMLFormElement;
    
    let toApiJSON = formToApiJson(form);

    const requestOptions = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(toApiJSON)
    };

    await fetch('/API/config', requestOptions)
}




export default function TopicInfo() {
    const general=configTemplate["general"]
    const notifications=configTemplate["notifications"]
    return (  
        <>     
        {/* General Settings */}
            <form onSubmit={onSubmit}>
                    <h1>General</h1>
                    <For each={Object.keys(general)}>
                        {(key) => {
                            const id=`general.${key}`
                            const input_object = general[key as keyof typeof general]
                            return (
                            <>
                                <label for={id}>{input_object["textLabel"]}</label>
                                <TextInput id={id} topicName={``} onInput={handleInput} value={(config as any)["general"][key]} typeData={input_object["type"]} required={"required" in input_object ? input_object["required"] : false}/>
                            </>
                            );
                        }}
                    </For>

                    <h1>Notifications methods</h1>
                    <For each={Object.keys(notifications)}>
                        {(notification) => {
                            const obj_notifications=notifications[notification as keyof typeof notifications]
                            return (
                            <>
                                <h2>{notification}</h2>
                               <For each={Object.keys(obj_notifications)}>
                                    {(key) => {
                                        const id=`notifications.${notification}.${key}`
                                        const input_object = obj_notifications[key as keyof typeof obj_notifications]
                                        return (
                                        <>
                                            <label for={id}>{input_object["textLabel"]}</label>
                                            <TextInput id={id} topicName={``} onInput={handleInput} value={(config as any)["notifications"][notification][key]} typeData={input_object["type"]} required={input_object["required"]}/>
                                        </>
                                        );
                                    }}
                                </For>
                            </>
                            );
                        }}
                    </For>
                <button type="submit">Submit</button>
            </form>
        </>
    );
}
