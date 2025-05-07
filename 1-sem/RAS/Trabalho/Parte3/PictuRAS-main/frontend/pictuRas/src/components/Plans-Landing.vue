<template>
    <div class="plan-box" :class="planType">
        <h2>{{ title }}</h2>
        <ul>
            <li v-for="feature in features" :key="feature">{{ feature }}</li>
        </ul>
        <div class="plan-footer">
            <h3>{{ price }}</h3>
            <Button1 @click="onChoosePlan" label=" Prosseguir →"></Button1>
        </div>
    </div>
</template>

<script>

import Button1 from './Button-style1.vue';
import { useRouter } from 'vue-router';


const router = useRouter();
export default {
    name: "PlanCard",
    components:{
        Button1,
    },
    props: {
        title: { type: String, required: true },
        features: { type: Array, required: true },
        price: { type: String, required: true },
        planType: { type: String, required: true },
    },
    methods:{
        onChoosePlan() {
            
            this.$router.push(`/login`);
        },
    }
};
</script>

<style scoped>
.plan-box {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: rgba(0, 0, 0, 0.25) 0px 4px 6px;
    text-align: center;
    width: 300px;
    height: 350px;
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.plan-box h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.plan-box ul {
    list-style-type: none;
    text-align: start;
    padding: 0;
    width: 80%;
    margin-bottom: 1rem;
    flex-grow: 1;
    width: 90%;
    align-self: center;
}

.plan-footer {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: auto;
}

.plan-footer h3 {
    margin-bottom: 1rem;
    font-size: 1.2rem;
    font-weight: bold;
}



.free-plan {
    border: 2px solid #007bff;
}

.Monthly-plan {
    border: 2px solid #8a2be2;
}

.Annual-plan {
    border: 2px solid #d415cb;
}

.Diary-plan {
    border: 2px solid #ffb107;
}



.plan-box button:hover {
    opacity: 0.9;
}
</style>
