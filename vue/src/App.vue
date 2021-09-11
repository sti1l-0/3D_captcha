<template>
  <div>
    <h1>拖动鼠标，旋转图像，还原字符</h1>
    <div class="captcha">
      <model-obj
        ref="model"
        src="http://192.168.1.102/get_file"
        :controlsOptions="{ enablePan: false, enableZoom: false }"
        :lights="[
          {
            type: 'DirectionalLight',
            position: { x: 1, y: 1, z: 1 },
            color: 0x00ff00,
            intensity: 0.8,
          },
          {
            type: 'DirectionalLight',
            position: { x: -1, y: -1, z: -1 },
            color: 0xff0000,
            intensity: 0.8,
          },
        ]"
        @on-click="OnClick"
        @on-load="OnLoad"
      >
      </model-obj>
    </div>
    <div class="cap_result">
      <h2>验证{{ pass }}</h2>
    </div>
  </div>
</template>

<script>
import { ModelObj } from "vue-3d-model";

export default {
  data() {
    return {
      loading: true,
      pass: "不通过",
      token: 0,
    };
  },
  methods: {
    OnLoad() {
      this.loading = false;
    },
    OnClick() {
      console.log(
        this.$refs.model.camera.position.x,
        this.$refs.model.camera.position.y,
        this.$refs.model.camera.position.z
      );
      this.$axios
        .post("http://192.168.1.102/check", {
          posx: this.$refs.model.camera.position.x,
          posy: this.$refs.model.camera.position.y,
          posz: this.$refs.model.camera.position.z,
        })
        .then((response) => (this.pass = response.data));
    },
  },
  components: {
    ModelObj,
  },
};
</script>

<style scoped>
div .captcha {
  height: 40%;
  width: 40%;
}
div .cap_result {
  background: #f00;
  width: fit-content;
}
</style>