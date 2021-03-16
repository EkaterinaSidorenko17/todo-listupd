<template>
  <v-layout row wrap justify-center>
    <v-flex xs8 class="pb-1">
      <new-todo-form @add="addTodo" />
    </v-flex>
    <v-flex v-for="todo of todoList" :key="todo.id" xs8 class="my-1">
      <todo-item :todo="todo" @delete="deleteTodo" />
    </v-flex>
  </v-layout>
</template>

<script>
import NewTodoForm from '../components/NewTodoForm'
import TodoItem from '../components/TodoItem'
export default {
  components: { TodoItem, NewTodoForm },
  methods: {
    addTodo(newTodo) {
      const id = this.todoList.length
        ? Math.max.apply(
            null,
            this.todoList.map(item => item.id)
          ) + 1
        : 1
      this.todoList.unshift({
        id,
        createdDate: new Date().toISOString().substr(0, 10),
        done: false,
        ...newTodo
      })
    },
    deleteTodo(todoId) {
      this.todoList = this.todoList.filter(item => item.id !== todoId)
    }
  }
}
</script>
