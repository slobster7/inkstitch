/*
 * Authors: see git history
 *
 * Copyright (c) 2010 Authors
 * Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
 *
 */
import { createWebHashHistory, createRouter } from 'vue-router'
const routes = [
    {
        path: '/simulator',
        name: 'simulator',
        component: () => import('../components/Simulator.vue')
    },
    {
        path: '/install',
        name: 'install',
        component: () => import('../components/InstallPalettes.vue')
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('../components/NotFound.vue')
    },
]
const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
