<template>
    <div class=" test-black p-5" style="width:260px;">
        <h4>{{ title }}</h4>
        <ul class="nav nav-pils flex-column">
            <li
                v-for="item in items" :key="item.route" class="nav-items mb-1"
            >
            <RouterLink :to="item.route" class="nav-link text-black"> 
                
                {{ item.label }}
            </RouterLink>

        </li>
        </ul>
    </div>
</template>
<script setup>

import { RouterLink } from "vue-router";

defineProps({
    title: {
        type : String, 
        default: "Placement Portal"
    },
    items: {
        type: Array,
        default:()=>[]
    }
})
    

</script>