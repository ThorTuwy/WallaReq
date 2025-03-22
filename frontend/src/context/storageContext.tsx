import { createSignal } from "solid-js";
import { createStore } from "solid-js/store"

import { TopicsToCheck } from "../auto-generated-types/topicsToCheck"

const [topics, setTopics] = createStore({} as TopicsToCheck);
const [topicNameSignal, setTopicName] = createSignal("")

export default function getTopics() {
  return { topics, setTopics,topicNameSignal,setTopicName };
}
