(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["pages-index-index"],{"455b":function(t,e,n){"use strict";n.d(e,"b",(function(){return a})),n.d(e,"c",(function(){return o})),n.d(e,"a",(function(){return i}));var i={uniSection:n("701c").default,uniList:n("52eb").default,uniListItem:n("f51d").default},a=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-uni-view",{staticClass:"content"},[n("cu-custom",{attrs:{bgColor:"bg-blue",isBack:!1}}),n("v-uni-view",{staticStyle:{"text-align":"center"}},[n("v-uni-image",{staticClass:"logo",attrs:{src:t.getAvatar()}}),n("v-uni-view",{staticStyle:{"margin-bottom":"10px"}},[n("span",{staticStyle:{"font-size":"20px"}},[t._v(t._s(t.settings["login.site_name"]||"后台管理系统"))])]),n("v-uni-view",{staticStyle:{"margin-bottom":"10px"}},[n("span",{staticStyle:{"font-size":"16px"}},[t._v("欢迎使用")])])],1),t.userInfo&&t.userInfo.name?n("v-uni-view",[n("uni-section",{attrs:{type:"line",title:"我的信息"}},[n("uni-list",[n("uni-list-item",{attrs:{title:"姓名",rightText:t.userInfo.name}}),n("uni-list-item",{attrs:{title:"手机号",rightText:t.userInfo.mobile}}),n("uni-list-item",{attrs:{title:"部门名称",rightText:t.userInfo.dept_info&&t.userInfo.dept_info.dept_name}}),n("uni-list-item",{attrs:{title:"角色",rightText:t.userInfo.role_info&&t.userInfo.role_info[0]&&t.userInfo.role_info[0].name}})],1)],1),n("v-uni-view",{staticStyle:{margin:"20px","margin-top":"40px"}},[n("br"),n("v-uni-button",{staticStyle:{"border-radius":"30px"},attrs:{type:"default"},on:{click:function(e){arguments[0]=e=t.$handleEvent(e),t.logout.apply(void 0,arguments)}}},[t._v("退出登录")])],1)],1):n("v-uni-view",{staticStyle:{"text-align":"center"}},[n("v-uni-text",{staticClass:"title"},[t._v("请进行登录！")])],1)],1)},o=[]},"56b7":function(t,e,n){"use strict";n.r(e);var i=n("f21f"),a=n.n(i);for(var o in i)["default"].indexOf(o)<0&&function(t){n.d(e,t,(function(){return i[t]}))}(o);e["default"]=a.a},"57f7":function(t,e,n){var i=n("d069");i.__esModule&&(i=i.default),"string"===typeof i&&(i=[[t.i,i,""]]),i.locals&&(t.exports=i.locals);var a=n("4f06").default;a("64b10216",i,!0,{sourceMap:!1,shadowMode:!1})},"67aa":function(t,e,n){"use strict";n.r(e);var i=n("455b"),a=n("56b7");for(var o in a)["default"].indexOf(o)<0&&function(t){n.d(e,t,(function(){return a[t]}))}(o);n("9f5e");var r=n("f0c5"),s=Object(r["a"])(a["default"],i["b"],i["c"],!1,null,"2f17e0c9",null,!1,i["a"],void 0);e["default"]=s.exports},"9f5e":function(t,e,n){"use strict";var i=n("57f7"),a=n.n(i);a.a},d069:function(t,e,n){var i=n("24fb");e=i(!1),e.push([t.i,".content[data-v-2f17e0c9]{\r\n  /* display: flex; */flex-direction:column;align-items:center;justify-content:center}.logo[data-v-2f17e0c9]{height:%?200?%;width:%?200?%;margin-top:%?150?%;margin-left:auto;margin-right:auto;margin-bottom:%?50?%}.text-area[data-v-2f17e0c9]{display:flex;justify-content:center}.title[data-v-2f17e0c9]{font-size:%?36?%;color:#8f8f94}uni-button[data-v-2f17e0c9]::after{border:none}",""]),t.exports=e},f21f:function(t,e,n){"use strict";n("7a82");var i=n("4ea4").default;Object.defineProperty(e,"__esModule",{value:!0}),e.default=void 0,n("d3b7");var a=i(n("c7eb")),o=i(n("1da1")),r=n("86bd"),s={data:function(){return{title:"Hello",loginUid:"",analysisData:{},loginData:{},userInfo:{},token:"",settings:uni.getStorageSync("third_settings")||{},isLoad:!1,optionsToken:""}},onShow:function(){var t=this;return(0,o.default)((0,a.default)().mark((function e(){return(0,a.default)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(!t.isLoad){e.next=3;break}return e.next=3,t.initData();case 3:case"end":return e.stop()}}),e)})))()},onLoad:function(t){var e=this;return(0,o.default)((0,a.default)().mark((function n(){return(0,a.default)().wrap((function(n){while(1)switch(n.prev=n.next){case 0:return console.log("options",t),e.loginUid=t.login_uid||"",e.optionsToken=t.token||"",e.optionsToken&&uni.setStorageSync("token",e.optionsToken),n.next=6,e.initData();case 6:e.isLoad=!0;case 7:case"end":return n.stop()}}),n)})))()},methods:{initData:function(){var t=this;return(0,o.default)((0,a.default)().mark((function e(){return(0,a.default)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(t.optionsToken&&uni.setStorageSync("is_webview",!0),t.token=uni.getStorageSync("token")||"",console.log("this.token",t.token),t.token){e.next=6;break}return uni.redirectTo({url:t.loginUid?"/pages/login/index?login_uid="+t.loginUid:"/pages/login/index"}),e.abrupt("return");case 6:return e.next=8,t.getUserInfo();case 8:t.getSettingsInfo(),t.loginUid&&uni.redirectTo({url:"/pages/scanLogin/index?login_uid="+t.loginUid});case 10:case"end":return e.stop()}}),e)})))()},getSettingsInfo:function(){var t=this;uni.request({url:r.API_URL+"api/init/settings/",success:function(e){2e3===e.data.code&&e.data.data&&(t.settings=e.data.data,uni.setStorageSync("third_settings",t.settings))}})},getUserInfo:function(){var t=this;return(0,o.default)((0,a.default)().mark((function e(){return(0,a.default)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.abrupt("return",new Promise((function(e,n){uni.request({url:r.API_URL+"api/system/user/user_info/",header:{Authorization:"JWT "+t.token},success:function(i){2e3===i.data.code&&i.data.data?(t.userInfo=i.data.data,e(i.data)):(uni.showToast({title:"登录失效，重新登陆！",icon:"error"}),uni.setStorageSync("token",""),uni.redirectTo({url:"/pages/login/index"}),n(i))},fail:function(t){uni.showToast({title:"请求失败:"+String(t),icon:"none"}),n(t)}})})));case 1:case"end":return e.stop()}}),e)})))()},getAvatar:function(){return this.userInfo&&this.userInfo.avatar?r.API_URL+this.userInfo.avatar:"/static/logo.png"},logout:function(){uni.setStorageSync("token",""),uni.redirectTo({url:"/pages/login/index"})}}};e.default=s}}]);