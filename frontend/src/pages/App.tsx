import type { Component } from 'solid-js';
import { Show } from 'solid-js';

import TopicInfo from "../components/TopicInfo";
import TopicsStatus from "../components/TopicsStatus";
import HeadderButtons from '../components/HeadderButtons';
import Welcome from '../components/Welcome';
import GeneralConfigs from '../components/GeneralConfigs';

import logo from '../assets/Wallareq.webp';
import styles from '../css/App.module.css';

import getTopics from "../context/storageContext";

const { topicNameSignal } = getTopics()!;

const App: Component = () => {

  return (
    <>

      <div class={styles.header}>
        <img class={styles.logo} src={logo} alt="Web logo"/>
        <div class={styles.headerButtons}>
          <HeadderButtons/>
        </div>
      </div>

      <div class={styles.content}>
        

          <div class={styles.container}>
            <TopicsStatus/>
          </div>

          <div class={styles["main-content"]}>
            <Show when={topicNameSignal() != "" } fallback={<Welcome/>}>
              <Show when={topicNameSignal() != "CONFIG" }>
                <TopicInfo/>
              </Show>
              <Show when={topicNameSignal() == "CONFIG" }>
                <GeneralConfigs/>
              </Show>
            </Show>
          </div>

        
      </div>

    </>
  );
};

export default App;
