<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios"
import Cookies from 'js-cookie';
import _ from 'lodash'

const forms = ref([])
const formToAdd = ref({});
const formToEdit = ref({});

const formById = computed(() => {
    return _.keyBy(forms.value, x => x.id)
})

async function fetchForms() {
    const r = await axios.get("/api/forms/")
    console.log("Форма выпуска")
    console.log(r.data)
    forms.value = r.data
}


async function onLoadClick() {
    await fetchForms()
}

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    await fetchForms()
})

async function onFormAdd() {
    const formData = new FormData();

    formData.set('form', formToAdd.value.form)

    await axios.post("/api/forms/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchForms()
}

async function onRemoveClick(form) {
    await axios.delete(`/api/forms/${form.id}/`);
    await fetchForms(); // переподтягиваю
}

async function onFormEditClick(form) {
    formToEdit.value = {
        ...form
    };
}

async function onUpdateForm() {
    console.log(formToEdit)

    const formData = new FormData();
    Object.entries(formToEdit.value).forEach(([key, value]) => {
        if (value != null) formData.set(key, value);
    });
    try {
        await axios.put(
            `/api/forms/${formToEdit.value.id}/`,
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
    await fetchForms();
}
</script>


<template>
    <form @submit.prevent.stop="onFormAdd">
        <div class="row field">
            <div class="col-auto">
                <div class="form-floating">
                    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                    <input type="text" class="form-control" v-model="formToAdd.form" required />
                    <label for="floatingInput">Форма выпуска</label>
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
    <div v-for="item in forms" class="patient-item">
        <div class="row">
            <div class="col ">
                <b>{{ item.form }}</b>
            </div>
        </div>
        <button class="btn btn-success red-item" @click="onFormEditClick(item)" data-bs-toggle="modal"
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
                                <input type="text" class="form-control" v-model="formToEdit.form" />
                                <label for="floatingInput">Форма выпуска</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateForm">
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
