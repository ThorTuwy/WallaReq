import { createContext, useContext, createSignal, type Accessor, type Setter } from "solid-js";
import { createStore,type SetStoreFunction } from "solid-js/store"


export type query = {
  keywords: string,
  order_by: string,
  is_shippable: boolean,
  max_sale_price: number
  min_sale_price: number
  category_ids: number
  latitude: number
  longitude: number
  condition: string
}

export type Topics = {
  enabled: boolean,
  name: string,
  querys:query[]
  ntfy: string[]
}

const [topics, setTopics] = createStore({} as Topics);
const [topicNameSignal, setTopicName] = createSignal("")

export default function getTopics() {
  return { topics, setTopics,topicNameSignal,setTopicName };
}
