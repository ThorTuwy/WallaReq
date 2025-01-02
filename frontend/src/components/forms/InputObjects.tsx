import { splitProps,For } from 'solid-js';

function parseValue(value:any){
    if(value == undefined){
      return "";
    }
    return value;
}

type option = {
    value: string
    text: string
}

export default function headderButtons(props:any) {
    const [data] = splitProps(props, ["id","topicName","onInput","value","typeData","required","options"]);

    if(data.typeData==="select"){
        
        
        if (parseValue(data.value) === "") {
            data.value = data.options[0].value;
        }
        
        return(
            <>
            <select name={data.id} id={data.id} 
            value={parseValue(data.value)}
            onInput={(event) => data.onInput(event.currentTarget,data.topicName)}>
                <For each={data.options}>
                    {(option:option) => (
                        <option value={option.value}>{option.text}</option>
                    )}
                </For>
            </select>
            </>
        )
    }

    //This is valid for checkbox and text inputs
    return(
        <>
        <input 
            required={data.required}
            type={data.typeData} id={data.id} name={data.id}
            value={parseValue(data.value)}
            checked={parseValue(data.value)}
            onInput={(event) => data.onInput(event.currentTarget,data.topicName)}>
        </input>
        </>
    )
}