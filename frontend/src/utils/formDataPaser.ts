//This convert the formData (ej: "general.config":500) to a JSON object



function isNumber(value?: string | number): boolean{
    return ((value != null) &&
            (value !== '') &&
            !isNaN(Number(value.toString())));
}


function setValue(subApiJSON:any,multiKey:string,value:any){
    const keys = multiKey.split('.');
    for (let i=0;i<keys.length-1;i++){
        let key:string|number=keys[i]

        //If the key is a number, it means that the key is the index of the array
        if(isNumber(keys[i+1]) && !subApiJSON[key]){
            subApiJSON[key]=[]
        }
        else{
            
            if(isNumber(key)){
                key=Number(key)
            }
    
            if(!subApiJSON[key]){
                subApiJSON[key]={}
            }
        }
        

        subApiJSON=subApiJSON[key]
    }
    
    if(!subApiJSON[keys.at(-1)!]){
        subApiJSON[keys.at(-1)!]=value
        return
    }
    else{
        throw new Error("The key "+keys.at(-1)+" already exists in the JSON object")
    }
}



export function formToApiJson(form: HTMLFormElement) {

    const apiJSON: any = {};

    const inputs = form.querySelectorAll('input');
    inputs.forEach((input: HTMLInputElement) => {
        const multiKey = input.id;
        if (input.type === 'checkbox') {
            setValue(apiJSON,multiKey,input.checked)
            return
        }
        if(multiKey==="ignore"){
            return
        }
        setValue(apiJSON,multiKey,input.value)
    });

    const selects = form.querySelectorAll('select');
    selects.forEach((select: HTMLSelectElement) => {
        const multiKey = select.id;
        setValue(apiJSON,multiKey,select.value)
    });

    return apiJSON;
}