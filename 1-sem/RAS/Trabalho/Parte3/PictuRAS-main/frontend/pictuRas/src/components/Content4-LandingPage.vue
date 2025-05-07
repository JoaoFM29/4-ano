<template>
  <div class="content4-layout">
    <div class="content4-init">
      <p class="p4-1">Plans</p>
      <h3 class="h4-1">Start using PictuRAS</h3>
      <p class="p4-2">Choose the perfect plan to unlock your creative potential.</p>
    </div>
    <div class="content4-plans">
      <div class="plan-container">
    <PlanCard
        title="Free"
        :features="[
            '5 Operations per day',
            'Images of limited sizes',
            '3 Downloads per day',
            'Low-resolution downloads up to 1GB limit',
            'Tool limitations'
        ]"
        price="Free"
        planType="free-plan"
        :isActive="currentPlan === 'free'"
       
    />
    <PlanCard
        title="Basic"
        :features="[
            'Unlimited operations per day',
            'Images of all sizes',
            'Limited downloads per day',
            'Unlimited HD downloads',
            'Tool limitations'
        ]"
        price="€15.00"
        planType="Annual-plan"
        :isActive="currentPlan === 'monthly'"
        
    />
    <PlanCard
        title="Premium"
        :features="[
            'Unlimited operations per day',
            'Images of all sizes',
            'Unlimited downloads per day',
            'Unlimited HD downloads',
            'Access to all tools'
        ]"
        price="€10.99"
        planType="Monthly-plan"
        :isActive="currentPlan === 'annual'"
        
    />
    <PlanCard
        title="Enterprise"
        :features="[
            'Unlimited operations per day',
            'Images of all sizes',
            'Unlimited downloads per day',
            'Unlimited HD downloads',
            'Access to all tools'
        ]"
        price="€20.99"
        planType="Diary-plan"
        :isActive="currentPlan === 'annual'"
       
    />
</div>
    </div>
  </div>
</template>

<script>
import PlanCard from '../components/Plans-Landing.vue';


export default {
  name: 'Content4',
  components: { PlanCard },
  data() {
    return {
      currentPlan: 'free',
    };
  },
};
</script>

<style scoped>
/* Content 4 */

.content4-layout {
    background-color: rgba(255, 255, 255, 0.534);
    display: flex;
    min-height: 80vh;
    flex-direction: column;
}

.content4-init {
  text-align: center; 
  width: 100%;
  padding: 2rem 1rem; 
  height: 20vh;
  padding-bottom: 0;
  font-family: Arial, Helvetica, sans-serif; 
}

.p4-1 {
  font-size: 0.8rem; 
  font-weight: bold; 
  letter-spacing: 1px;
  color: #555;
  text-transform: uppercase; 
}

.h4-1 {
  font-size: 1.4rem; 
  font-weight: bold; 
  color: #333; 
}

.p4-2 {
  font-size: 1rem; 
  line-height: 1.5; 
  max-width: 600px; 
  margin: 0 auto; 
}

.content4-plans {
  height: 60vh;
  width: 100%;
  background: linear-gradient(
    to top,
    #0057b3da,
    #70c5f9 30%,
    #ffffff 100%
  );
  padding-bottom: 2em;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row !important;
}

.plan-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 1500px;
}



</style>
  