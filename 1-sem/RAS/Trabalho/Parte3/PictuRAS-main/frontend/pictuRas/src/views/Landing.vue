<template>
    <div class="main-layout">
        <Navbar id="nav"></Navbar>
        <div class="landing-container">

            <!-- Content 1 -->
            <Content1 :isPlaying="isPlaying" @toggleVideo="toggleVideo"  @content1Visible="handleContent1Visibility" />
            <!-- Content 2 -->
            <Content2 :isPlaying="isPlaying" @toggleVideo="toggleVideo" />
            
            <!-- Content 3-->
            <Content3></Content3>

            <!-- Content 4 -->
            <Content4></Content4>

            <!-- Content5 -->
             <Content5></Content5>

            <!-- Content6 -->
            <Content6 @content6Visible="handleContent6Visibility"></Content6>


      </div>
      <Footer :showFooter="showFooter" />
    </div>
</template>
  
<script>

    import Navbar from '../components/Navbar.vue';
    import Content1 from '../components/Content1-LandingPage.vue';
    import Content2 from '../components/Content2-LandingPage.vue';
    import Content3 from '../components/Content3-LandingPage.vue';
    import Content4 from '../components/Content4-LandingPage.vue';
    import Content5 from '../components/Content5-LandingPage.vue';
    import Content6 from '../components/Content6-LandingPage.vue';
    import Button1 from '../components/Button-style1.vue';
    import Button2 from '../components/Button-style2.vue';
    import Footer from "../components/FooterLanding.vue";

    export default {
    name: 'Landing',
    components: {
        Navbar,
        Content1,
        Content2,
        Content3,
        Content4,
        Content5,
        Content6,
        Button1,
        Button2,
        Footer
    },
    data() {
        return {
            isPlaying: true, 
            showFooter: false,
            content1Visible: true,
            content6Visible: false,
        };
    },
    methods: {
        toggleVideo() {
        this.isPlaying = !this.isPlaying;
        },

        handleContent1Visibility(isVisible) {
            this.content1Visible = isVisible;
            this.updateFooterVisibility();
        },
        handleContent6Visibility(isVisible) {
            this.content6Visible = isVisible;
            this.updateFooterVisibility();
        },
        updateFooterVisibility() {
            this.showFooter = !this.content1Visible || !this.content6Visible;
        },
    },
    };

</script>
  
  <style scoped>
  

  /* Content 1 */
  
  .main-layout {
      display: flex;
      flex-direction: column;
      grid-template-areas:
        "nav nav"
        ". .";
      overflow: auto;
      gap:0px;
      overflow-x: hidden;
  }

  #nav{
    grid-area: nav;
    
  }

/* Content 6 */
.margin-bot{
    height: 15vh;
    width: 100%;

}


  </style>
  