import { splitProps } from 'solid-js';

function parseValue(value:any){
    if(value == undefined){
      return "";
    }
    return value;
}

export default function headderButtons(props:any) {
    const [data] = splitProps(props, ["id","topicName","onInput","value", "typeData","required"]);

    let required;
    if(data.required===true){
        return(
            <>
            
            <input 
                required
                type={data.typeData} id={data.id} name={data.id}
                value={parseValue(data.value)}
                checked={parseValue(data.value)}
                onInput={(event) => data.onInput(event.currentTarget,data.topicName)}>
            </input>
    
    
    
            </>
        )
    }

    

    return(
        <>
        
        <input
            type={data.typeData} id={data.id} name={data.id}
            value={parseValue(data.value)}
            checked={parseValue(data.value)}
            onInput={(event) => data.onInput(event.currentTarget,data.topicName)}>
        </input>



        </>
    )
}