<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios"
import Cookies from 'js-cookie';
import _ from 'lodash'

const actions = ref([])
const actionToAdd = ref({});
const actionToEdit = ref({});

const formById = computed(() => {
    return _.keyBy(actions.value, x => x.id)
})

async function fetchActions() {
    const r = await axios.get("/api/actions/")
    console.log("Терапевтическое действие")
    console.log(r.data)
    actions.value = r.data
}


async function onLoadClick() {
    await fetchActions()
}

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    await fetchActions()
})

async function onActionAdd() {
    const formData = new FormData();

    formData.set('action', actionToAdd.value.action)

    await axios.post("/api/actions/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchActions()
}

async function onRemoveClick(action) {
    await axios.delete(`/api/actions/${action.id}/`);
    await fetchActions(); // переподтягиваю
}

async function onActionEditClick(action) {
    actionToEdit.value = {
        ...action
    };
}

async function onUpdateAction() {
    console.log(actionToEdit)

    const formData = new FormData();
    Object.entries(actionToEdit.value).forEach(([key, value]) => {
        if (value != null) formData.set(key, value);
    });
    try {
        await axios.put(
            `/api/actions/${actionToEdit.value.id}/`,
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            }
        );
    } catch (error) {
        console.error("Ошибка при обновлении записи:", error);
    }
    await fetchActions();
}
</script>


<template>
    <form @submit.prevent.stop="onActionAdd">
        <div class="row field">
            <div class="col-auto">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input type="text" class="form-control" v-model="actionToAdd.action" required />
                    <label for="floatingInput">Терапевтическое действие</label>
                </div>
            </div>
        </div>
        <div class="row field">
            <div class="col-auto">
                <button class="btn btn-primary">
                    Добавить
                </button>
            </div>
        </div>
    </form>
    <div v-for="item in actions" class="patient-item">
        <div class="row">
            <div class="col ">
                <b>{{ item.action }}</b>
            </div>
        </div>
        <button class="btn btn-success red-item" @click="onActionEditClick(item)" data-bs-toggle="modal"
            data-bs-target="#editPatientModal">
            <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger del-item" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
        </button>
    </div>

    <button @click="onLoadClick">Загрузить</button>


    <div class="modal fade" id="editPatientModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактирование
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-auto">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="actionToEdit.action" />
                                <label for="floatingInput">Терапевтическое действие</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateAction">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

</template>


<style lang="scss" scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css");

.patient-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
    display: flex;
    align-items: center;
}

.del-item {
    justify-content: right;
    margin-left: 10px;
}

.red-item {
    justify-content: right;
    margin-left: auto;
}

.navbar-nav {
    justify-content: right;
    margin: 1rem;
}

.field {
    margin-bottom: 10px;
}
</style>
