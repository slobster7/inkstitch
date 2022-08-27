<!--

  Authors: see git history

  Copyright (c) 2010 Authors
  Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

-->
<template>
<!DOCTYPE html>
<html>
<title>Install Ink/Stitch Palettes</title>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<component is="style" scoped>

.card {
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  width: 80%;
  border-radius: 5px;
}
.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
.container {
  padding: 2px 16px;
}
</component>
</head>
<body>

<h2>{{ $gettext("Install Palettes") }}</h2>

<div class="card" v-if="step == 'pick'" key="pick" rounded="lg" :loading="installing" :disabled="installing">
  <div class="container">
        <p class="card-text"><translate>Ink/Stitch can install palettes for Inkscape matching the thread colors from popular machine embroidery thread manufacturers.
        </translate></p>
        <label for="installPalattes">Default Inkscape directory:</label>
        <h2>
        {{ thisPath }}
        </h2>
        <p class="card-text">
         {{ $gettext("If you are not sure which file path to choose, click on install directly. In most cases Ink/Stitch will guess the correct path.") }}
        </p>

        <button type="button" v-on:click="install">Install</button>
        <button type="button" v-on:click="close">Cancel</button>
  </div>
</div>
<div class="card" v-if="step == 'done'" key="done">
  <div class="container">
        <p class="card-text"><translate>
          Installation Completed
        </translate></p>
        <p class="card-text"><translate>
          Inkscape palettes have been installed. Please restart Inkscape to load the new palettes.
        </translate></p>
        <button type="button" v-on:click="close">Done</button>
  </div>
</div>
<div class="card"  v-if="step == 'error'" key="error">
  <div class="container">
    <p class="card-text"><translate>
        Installation Failed
        </translate></p>
        <p class="card-text"><translate>
        Inkscape add-on installation failed
        </translate></p>
        <p class="card-text">
        {{ error }}
        </p>
        <button type="button" v-on:click="retry"><translate>Try again</translate></button>
        <button type="button" v-on:click="close">Cancel</button>
  </div>
</div>
</body>
</html>
</template>
<script>
import isServer from '../../lib/api.js'
const inkStitch = isServer

export default {
  name: "InstallPalettes",
  data: function () {
    return {
      path: null,
      installing: false,
      step: "pick",
      error: null,
      thisPath: null
    }
  },
  methods: {
    install() {
      this.installing = true
      inkStitch.post('install/palettes', {path: this.path.path || this.path.name}).then(response => {
        this.step = "done"
      }).catch(error => {
        this.step = "error"
        this.error = error.response.data.error
      }).then(() => {
        this.installing = false
      })
    },
    close() {
      window.close()
    },
    retry() {
      this.installing = false
      this.step = "pick"
    }
  },
  created: function () {
    inkStitch.get("install/default-path").then(response => {
      this.path = new File([""], response.data, {})
      this.thisPath = response.data
    })
  }
}
</script>

<style scoped>

</style>

