import { splitProps,For,createSignal,createEffect } from 'solid-js';
import { createStore,produce, } from "solid-js/store"

import styles from '../../css/App.module.css';
import Trash from 'lucide-solid/icons/trash';
import Plus from 'lucide-solid/icons/plus';

type option = {
    value: any;
    text: string;
};

function parseValue(value:any){
    if(value == undefined){
      return "";
    }
    return value;
}







export default function headderButtons(props:any) {
    const [data] = splitProps(props, ["id","topicName","onInput","value","typeData","required","options"]);

    const [processedValue, setProcessedValue] = createSignal(parseValue(data.value));

    const cleanerOptions = (options:any) => {
        let newOptions:option[]=[]

        options.forEach((option:string[]) => {
            newOptions.push({value:option[0],text:option[1]})
        })

        return newOptions
    }

    createEffect(() => {
        const value=parseValue(data.value);
        if (data.typeData==="select" && value === "") {
            const newOptions=cleanerOptions(data.options);
            setProcessedValue(newOptions[0]["value"]);
        }
        else{
            setProcessedValue(value);
        }
    });

    if(data.typeData==="select"){
        type option = {
            value: string
            text: string
        }

        //data.options is a array that cotaints arrays with value (at index 0) and text (at index 1)
        
        


        
        return(
            <>
            <select id={data.id} name={data.id}
            value={processedValue()}
            onInput={(event) => data.onInput(event.currentTarget,data.topicName)}>
                <For each={cleanerOptions(data.options)}>
                    {(option:option) => (
                        <option value={option["value"]}>{option["text"]}</option>
                    )}
                </For>
            </select>
            </>
        )
    }

    if(data.typeData==="stringArray"){
        //TODO: Woa, this code is garbage, I need to clean it up
        let newValue:string[]=[]
        if(processedValue()!=""){
            newValue=processedValue()
        }
        const [valueSig, setvalueSig] = createSignal(newValue);
        createEffect(() => {
            setvalueSig(parseValue(data.value));
        });
    

        const removeString = (e:MouseEvent) => {
            const button = e.currentTarget as HTMLButtonElement;
            const parent = button.parentElement!;
            const index = Array.from(parent.parentElement!.children).indexOf(parent);
            setvalueSig(valueSig().filter((_, i) => i !== index));
        }

        const addString = (e:MouseEvent) => {
            const button = e.currentTarget as HTMLButtonElement;
            const input = button.previousElementSibling as HTMLInputElement;
            
            setvalueSig([...valueSig(), input.value]);
            input.value = "";
        }              

        const addInputString = (channel:string,index:number) => {
            return (
                <div style={{display: "flex"}}>
                    <input disabled type="text" id={data.id+`.${index}`} name={"array."+data.id} value={channel}/>
                    <button class={[styles.actionButton, styles.remove, styles.iconButton].join(" ")} type="button" onclick={(e) => removeString(e)}>
                        <Trash/>
                    </button>
                </div>
            )
        }
        return(
            <>
            <For each={valueSig()}>
                {(strElement,index) => (
                    <>
                    <div style={{display: "flex"}}>
                        {addInputString(strElement,index())}
                    </div>
                    </>
                )}
            </For>
            <div style={{display: "flex"}}>
                <input type="text" id="ignore" name={data.id+"_new"}/>
                <button class={[styles.actionButton, styles.add, styles.iconButton].join(" ")} type="button" onclick={(e) => addString(e)}>
                    <Plus/>
                </button>
            </div>
            </>
        )
    }

    //This is valid for checkbox and text inputs
    return(
        <>
        <input 
            required={data.required}
            type={data.typeData} id={data.id} name={data.id}
            value={processedValue()}
            checked={processedValue()}
            onInput={(event) => data.onInput(event.currentTarget,data.topicName)}>
        </input>
        </>
    )
}