<template>
    <div class="faq-container">
      <h2 class="faq-title">Have questions? We have answers.</h2>
      <div v-for="(faq, index) in faqs" :key="index" class="faq-item">
        <div class="faq-question"  :class="{ active: faq.isOpen }"  @click="toggleAnswer(index)">
          <p>{{ faq.question }}</p>
          <span class="faq-icon">
            <font-awesome-icon :icon="faq.isOpen ? 'fa-minus' : 'fa-plus'" />
          </span>
        </div>
        <div v-if="faq.isOpen" class="faq-answer">
          <p>{{ faq.answer }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons';
  import { library } from '@fortawesome/fontawesome-svg-core';

  
  library.add(faPlus, faMinus);
  
  export default {
    name: 'Content5',
    components: {
      FontAwesomeIcon,
    },
    data() {
      return {
        faqs: [
            {
                question: 'How much does PictuRAS cost?',
                answer: 'PictuRAS plans start at €9.99/month (VAT included). Learn more on our pricing page.',
                isOpen: false,
            },
            {
                question: 'Does PictuRAS support editing high-resolution images?',
                answer: 'Absolutely! PictuRAS supports editing high-resolution images, ensuring professional-quality results.',
                isOpen: false,
            },
            {
                question: 'Is PictuRAS suitable for beginners?',
                answer: 'Yes, PictuRAS offers an intuitive interface and tutorials, making it perfect for beginners and professionals alike.',
                isOpen: false,
            },
            {
                question: 'Is PictuRAS available on mobile devices?',
                answer: 'Currently, PictuRAS is available on desktop only, but a mobile version is in development.',
                isOpen: false,
            },
            {
                question: 'Can PictuRAS edit multiple images at the same time?',
                answer: 'Yes, PictuRAS includes a batch editing feature that allows you to apply adjustments like brightness, contrast, and filters to multiple images simultaneously. This saves time and ensures consistency across your edits.',
                isOpen: false,
            },
            {
                question: 'Does PictuRAS have a free version?',
                answer: 'Yes, PictuRAS offers a free plan with limited features. Upgrade anytime to unlock premium tools.',
                isOpen: false,
            },
        ],
      };
    },
    methods: {
      toggleAnswer(index) {
        this.faqs[index].isOpen = !this.faqs[index].isOpen;
      },
    },
  };
  </script>
  
  <style scoped>
  .faq-container {
    width: 100%;
    margin: 2rem auto;
    display: flex;
    flex-direction: column;
    font-family: Arial, sans-serif;
    justify-content: center;
    align-items: center;
    padding-bottom: 5vh;
  }
  
  .faq-title {
    text-align: center;
    font-size: 1.3rem;
    margin-bottom: 3rem;
  }
  
  .faq-item {
    border-top: 0.3px solid black;
    width: 50%;
  }

  .faq-item:nth-last-child() {
    border-bottom: 0.3px solid black;
    width: 50%;
  }
  
  .faq-question {
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    padding: 0.5rem;
    font-weight: bold;
    background: #f9f9f9;
    transition: background-color 0.3s ease;
  }

  .faq-question.active {
  border-left: 3px solid #007bff;
}

  
  .faq-question:hover {
    background: #f1f1f1;
  }
  
  .faq-icon {
    font-size: 1.2rem;
  }
  
  .faq-answer {
    padding: 0.5rem;
    background: #fff;
  }
  </style>
  