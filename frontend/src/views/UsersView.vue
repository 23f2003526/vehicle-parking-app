<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const users = ref([])
const loading = ref(true)
const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

const searchQuery = ref('')

const filteredUsers = computed(() => {
    const q = searchQuery.value.toLowerCase()
    return users.value.filter(u =>
        u.id.toString().includes(q) ||
        u.name.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q)
    )
})

onMounted(async () => {
    try {
        const userResponse = await axios.get('/api/dashboard')
        userStore.setUserDetails(userResponse.data)
    } catch (error) {
        toast.error("Session Expired. Login Again.")
        userStore.logout()
        router.push('/login')
        return
    }

    if (!userStore.isAdmin) {
        router.push('/unauthorized')
        return
    }
    try {
        const res = await axios.get('/api/admin/users')
        users.value = res.data
    } catch (err) {
        console.error(err)
        toast.error('Failed to fetch users.')
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="container">
        <h2>Users</h2>

        <div v-if="loading" class="state">Loading...</div>
        <div v-else>
            <input v-model="searchQuery" type="text" placeholder="Search by ID, Name, or Email" class="search-input" />

            <div v-if="!filteredUsers.length" class="state">No users found</div>

            <div v-else class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Vehicles</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="u in filteredUsers" :key="u.id">
                            <td class="id">{{ u.id }}</td>
                            <td>{{ u.name }}</td>
                            <td class="email">{{ u.email }}</td>
                            <td>
                                <span class="role" :class="u.role">{{ u.role }}</span>
                            </td>
                            <td class="vehicles">
                                <div v-if="u.vehicles.length">
                                    <div v-for="v in u.vehicles" :key="v.id" class="vehicle">
                                        {{ v.license_plate }}
                                        <span class="type">{{ v.vehicle_type }}</span>
                                    </div>
                                </div>
                                <span v-else class="none">None</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<style scoped>
.search-input {
    margin-bottom: 1rem;
    padding: 6px;
    width: 300px;
    border: 1px solid #ccc;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
}

h2 {
    margin: 0 0 24px 0;
    font-size: 28px;
    font-weight: 500;
    color: #333;
}

.state {
    padding: 40px;
    text-align: center;
    color: #666;
    font-size: 18px;
}

.table-wrap {
    overflow-x: auto;
    border: 1px solid #e5e5e5;
    border-radius: 4px;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

th {
    background: #f8f9fa;
    padding: 12px 16px;
    text-align: left;
    font-weight: 500;
    font-size: 16px;
    color: #666;
    border-bottom: 1px solid #e5e5e5;
}

td {
    padding: 12px 16px;
    border-bottom: 1px solid #f0f0f0;
    font-size: 16px;
    vertical-align: top;
}

tr:last-child td {
    border-bottom: none;
}

.id {
    color: #666;
    font-family: monospace;
    font-size: 15px;
}

.email {
    color: #666;
    font-size: 15px;
}

.role {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.role.admin {
    background: #fee2e2;
    color: #dc2626;
}

.role.user {
    background: #f0f9ff;
    color: #0369a1;
}

.vehicles {
    min-width: 200px;
}

.vehicle {
    margin: 2px 0;
    font-size: 15px;
}

.type {
    color: #666;
    font-size: 14px;
}

.none {
    color: #999;
    font-size: 15px;
    font-style: italic;
}

@media (max-width: 768px) {
    .container {
        padding: 16px;
    }

    th,
    td {
        padding: 8px 12px;
    }

    .vehicles {
        min-width: 150px;
    }
}
</style>