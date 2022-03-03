<template>
  <div>
    <div id="captcha">
      <h1>拖动鼠标，旋转图像，还原字符</h1>
      <model-obj
        ref="model"
        src="/get_file"
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
          {
            type: 'DirectionalLight',
            position: { x: -1, y: 1, z: -1 },
            color: 0x0000ff,
            intensity: 0.8,
          },
        ]"
        @on-click="OnClick"
        @on-load="OnLoad"
      >
      </model-obj>
    </div>
    <div id="cap_result">
      <h2>验证{{ pass }}</h2>
    </div>
    <p id="github">
      恭喜验证通过~本项目的源码地址是
      <a href="https://github.com/sti1l-0/3D_captcha/tree/main/back_end">sti1l-0/3D_captcha</a>
    </p>
  </div>
</template>

<script>
import { ModelObj } from "vue-3d-model";

export default {
  data() {
    return {
      pass: "不通过",
      token: 0,
    };
  },
  methods: {
    OnLoad() {
      var xyz = this.Radius125()
      this.$refs.model.camera.position.x = xyz[0];
      this.$refs.model.camera.position.y = xyz[1];
      this.$refs.model.camera.position.z = xyz[2];
      console.log('asf')
      requestAnimationFrame(function(){});
    },
    Radius125(){
        var a = Math.random() * 120;
        var b = Math.random() * (125**2 - a**2)**0.5;
        var c = (125**2 - a**2 - b**2)**0.5
      return [a,b,c];
    },
    OnClick() {
      this.$axios
        .post("/check", {
          posx: this.$refs.model.camera.position.x,
          posy: this.$refs.model.camera.position.y,
          posz: this.$refs.model.camera.position.z
        })
        .then((response) => {
          this.pass = String(response.data)=='true'?'通过':'不通过'
          if(this.pass === '通过'){
            var t = document.getElementById('captcha');//选取id为test的元素
            t.style.display = 'none';	// 隐藏选择的元素
            t.style.background = '#00ff00';
            t = document.getElementById('github');//选取id为test的元素
            t.style.visibility = 'visible';	// 隐藏选择的元素
          }
        });
    },
  },
  components: {
    ModelObj,
  },
};
</script>

<style scoped>
  #captcha {
    height: 40%;
    width: 40%;
  }
  #cap_result {
    background: #f00;
    width: fit-content;
  }

  #github{
    visibility: hidden;
}
</style>