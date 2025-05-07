<template>
    <button :disabled="disabled || loading" class="loading-button">
        <span v-if="!loading">
            <slot>Submit</slot>
        </span>
        <span v-else class="spinner"></span>
    </button>
</template>

<script>
export default {
    name: 'LoadingButton',
    props: {
        loading: {
            type: Boolean,
            default: false
        },
        disabled: {
            type: Boolean,
            default: false
        }
    }
};
</script>

<style scoped>
.loading-button {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 2.5rem;
}

.spinner {
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>