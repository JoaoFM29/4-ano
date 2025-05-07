import { defineStore } from 'pinia'
import axios from 'axios'

export const useEditingToolStore = defineStore('editingTool', {
  state: () => ({
    tools: [],
    activeTool: null
  }),

  actions: {
    async fetchTools() {
      try {

        const response = await axios.get(`${import.meta.env.VITE_API_GATEWAY}/api/tools`)
        const fetchedTools = response.data.map((tool, index) => ({
          ...tool,
          active: false, // Add "active" field
          position: index // Add "position" field
        }))
        this.tools = fetchedTools
      } catch (error) {
        console.error('Failed to fetch tools:', error)
      }
    },

    addTool() {
      // Count the number of tools with the same name as the active tool
      const baseName = this.activeTool.name;
      const sameNameCount = this.tools.filter(tool => tool.name.startsWith(baseName)).length;
    
      // Create a copy of the active tool and modify its name if needed
      const newTool = JSON.parse(JSON.stringify(this.activeTool));
      if (sameNameCount > 0) {
        newTool.name = `${baseName} copy ${sameNameCount}`;
      }
    
      // Push the new tool to the tools array
      this.tools.push(newTool);
    },

    removeTool(name) {
      this.tools = this.tools.filter(tool => tool.name !== name)
      if (this.activeTool?.name === name) {
        this.activeTool = null
      }
    },

    setActiveTool(name) {
      this.activeTool = this.tools.find(tool => tool.name === name) || null
    },

    addParameter(toolName, parameter) {
      const tool = this.tools.find(t => t.name === toolName)
      if (tool) {
        tool.parameters.push(parameter)
      }
    },

    updateParameterValue(toolName, paramName, value) {
      const tool = this.tools.find(t => t.name === toolName)
      const param = tool?.parameters.find(p => p.name === paramName)
      if (param) {
        param.value = value
      }
    },
    async mergeTools(activeTools) {
      this.activeTool = null;
    
      // Ensure that active tools are renamed with "copy x" if needed
      const baseToolCounts = {}; // Tracks the number of tools per base name
      activeTools.forEach(tool => {
        const baseName = tool.name.split(" copy")[0].trim();
    
        // Initialize the count for this base name if not already present
        if (!baseToolCounts[baseName]) {
          baseToolCounts[baseName] = 0;
        }
    
        // Check for duplicate names within activeTools
        const sameNameCount = baseToolCounts[baseName]++;
        if (sameNameCount > 0) {
          tool.name = `${baseName} copy ${sameNameCount}`;
        }
    
        // Ensure the "id" field exists on all active tools
        if (!tool.hasOwnProperty("id")) {
          tool.id = null; // Assign null if no ID exists initially
        }
      });
    
      // Merge active tools into the fetched tools
      for (let i = 0; i < activeTools.length; i++) {
        let isMerged = false;
    
        for (let j = 0; j < this.tools.length; j++) {
          // Match by name
          if (this.tools[j].name === activeTools[i].name) {
            // Update the parameters if they exist
            if (activeTools[i].parameters && activeTools[i].parameters.length > 0) {
              this.tools[j].parameters = JSON.parse(JSON.stringify(activeTools[i].parameters));
            }
    
            // Update position and active status
            this.tools[j].position = i;
            this.tools[j].active = true;
    
            // Swap the current tool to the correct position
            const temp = this.tools[j];
            this.tools[j] = this.tools[i];
            this.tools[i] = temp;
    
            isMerged = true;
            break;
          }
        }
    
        // If no match found, add the active tool to the tools list at the correct position
        if (!isMerged) {
          activeTools[i].position = i;
          activeTools[i].active = true;
    
          // Ensure the "id" field exists on the new tool
          if (!activeTools[i].hasOwnProperty("id")) {
            activeTools[i].id = null; // Assign null if no ID exists initially
          }
    
          this.tools.splice(i, 0, activeTools[i]);
        }
      }
    
      // Reassign positions to maintain the correct order
      this.tools.forEach((tool, index) => {
        tool.position = index;
      });
    
      // Assign IDs to copies
      this.tools.forEach(tool => {
        // Check if the tool is a copy (contains " copy x")
        if (tool.name.includes(" copy")) {
          console.log(tool);
          const baseName = tool.name.split(" copy")[0].trim();
    
          // Find the base tool with the same base name
          const baseTool = this.tools.find(t => t.name === baseName);
          console.log(baseTool);
          // If a base tool exists, assign its ID to the copy
          if (baseTool) {
            tool.id = baseTool.id;
          }
          console.log(tool);
        }
      });
    },
    clear(){
      this.activeTool = null;
      this.tools= [];
    }
  },

  getters: {
    getTool: (state) => {
      return (name) => state.tools.find(tool => tool.name === name)
    },

    getParameterValue: (state) => {
      return (toolName, paramName) => {
        const tool = state.tools.find(t => t.name === toolName)
        return tool?.parameters.find(p => p.name === paramName)?.value
      }
    }
  }
})
