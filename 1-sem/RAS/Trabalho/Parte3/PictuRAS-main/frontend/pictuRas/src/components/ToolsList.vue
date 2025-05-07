<template>
  <div class="tools-list">
    <h1>Tools</h1>
    <draggable
      v-model="tools"
      tag="ul"
      :active="true"
      @change="updateList"
    >
      <template #item="{ element: tool }">
        <li
          :class="{ active: tool.active === true, premium: tool.premium === true }"
          @click="selectTool(tool.name)"
        >
          {{ tool.name }}
        </li>
      </template>
    </draggable>
  </div>
</template>


<script>
import { useEditingToolStore } from '../stores/EditingTool'
import { storeToRefs } from 'pinia'
import draggable from 'vuedraggable'
import { onMounted, ref } from 'vue'

export default {
  name: 'ToolsList',
  components: {
    draggable
  },
  setup() {
    const store = useEditingToolStore()
    const { tools, activeTool } = storeToRefs(store)

    // Local variable to store the previous state of the tools list
    const previousTools = ref([...tools.value])

    // Validation function for the tools list
    const validateList = (tools) => {
       // Filter the list to only include active tools
      const activeTools = tools.filter((tool) => tool.active)

      if (activeTools.length === 0) {
        return true // If no tools are active, the configuration is valid
      }

      // Validate the first active tool
      if (activeTools[0].input_type !== 'image') {
        return false // First active tool must have input_type 'image'
      }

      // Validate subsequent active tools
      for (let i = 1; i < activeTools.length; i++) {
        const prevTool = activeTools[i - 1]
        const currentTool = activeTools[i]

        // Check if the current tool's input_type matches the previous tool's output_type
        if (currentTool.input_type !== prevTool.output_type) {
          return false // Input type does not match previous output type
        }
      }

      return true // All active tools are valid
    }
    // Fetch tools when the component is mounted
    onMounted(async () => {
      // await store.fetchTools()
      previousTools.value = [...tools.value] // Save initial state
    })

    // Method to set the selected tool as active
    const selectTool = (name) => {
      store.setActiveTool(name)
    }

    // Method to handle the list update with validation
    const updateList = () => {
      const newList = [...tools.value] // Clone the updated list
      if (!validateList(newList)) {
        // If validation fails, roll back
        tools.value = [...previousTools.value]
        alert('Invalid configuration. Reverting to the previous list.')
        return
      }

      // If validation passes, update positions and save the state
      newList.forEach((item, index) => (item.position = index))
      previousTools.value = [...newList] // Update the previous state
    }

    return {
      tools,
      activeTool,
      selectTool,
      updateList
    }
  }
}
</script>

<style scoped>

.tools-list {
  padding: 1rem;
  background-color: #f7f7f7;
  /*width: 100%;*/
  height: 50vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-self: center;
  border-radius: 20px;
  border: 1px solid #000000;
  box-shadow: 0 0 6px #000000;
  overflow-y: scroll;
}

ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

li {
  padding: 0.5rem 1rem;
  cursor: pointer;
  margin: 0.25rem 0;
  border-radius: 4px;
}

li:hover {
  background-color: #f0f0f0;
}

li.active {
  font-weight: bold;
}

li.premium {
  color: gold; /* Yellow text for premium tools */

}
</style>
