<template>

    <div class="table-responsive">

        <table class="table table-hover align-middle mb-0">
            <thead >
                <tr>
                    <th v-for="column in columns" :key="column.key">
                        {{ column.label }}
                    </th>
                </tr>

            </thead>
            <tbody v-if="rows.length">
                <tr v-for="( row, rowIndex ) in rows" :key="row.id ?? rowIndex">
                    <td v-for="column in columns" :key="column.key">
                        <slot :name="`cell-${column.key}`" :row="row" :value="row[column.key]">
                            {{ row[column.key] }}
                        </slot>
                    </td>
                </tr>


            </tbody>

            <tbody v-else>
                <tr>
                    <td :colspan="columns.length" class="text-center text-muted py-4"> No data available</td>
                </tr>

            </tbody>

        </table>


    </div>

</template>

<script setup>

defineProps({
    columns:{
        type : Array,
        required: true
    },
    rows: {
        type: Array,
        default: ()=> []
    }
})

</script>