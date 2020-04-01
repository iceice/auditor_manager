<template>
  <div id="app">
    <el-container>
      <el-header style="height: 80px">学生信息管理系统</el-header>
      <el-container>
        <!-- 侧边栏 -->
        <el-aside width="200px">
          <el-menu default-active="1" class="el-menu-vertical-demo">
            <el-menu-item index="1">
              <i class="el-icon-user"></i>
              <span slot="title">学生信息</span>
            </el-menu-item>
            <el-menu-item index="2">
              <i class="el-icon-s-custom"></i>
              <span slot="title">教师信息</span>
            </el-menu-item>
            <el-menu-item index="3">
              <i class="el-icon-document"></i>
              <span slot="title">课程管理</span>
            </el-menu-item>
            <el-menu-item index="4">
              <i class="el-icon-setting"></i>
              <span slot="title">班级管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <!-- 主窗体 -->
        <el-container>
          <el-main>
            <!-- 面包屑导航 -->
            <el-breadcrumb separator-class="el-icon-arrow-right">
              <el-breadcrumb-item>首页</el-breadcrumb-item>
              <el-breadcrumb-item>学生信息</el-breadcrumb-item>
            </el-breadcrumb>
            <!-- 表单 -->
            <el-form :inline="true" style="margin-top:20px">
              <el-row :gutter="10">
                <el-col :span="10" style="text-align:left">
                  <el-form-item label="请输入">
                    <el-input placeholder="查询条件" style="width: 360px"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-button-group>
                    <el-button type="primary" icon="el-icon-search">查询</el-button>
                    <el-button type="primary" icon="el-icon-tickets">全部</el-button>
                    <el-button type="primary" icon="el-icon-circle-plus-outline">添加</el-button>
                  </el-button-group>
                </el-col>
                <el-col :span="3" style="text-align:right">
                  <el-upload>
                    <el-button type="primary">导入Excel</el-button>
                  </el-upload>
                </el-col>
                <el-col :span="3" style="text-align:left">
                  <el-button type="primary">导出Excel</el-button>
                </el-col>
              </el-row>
            </el-form>
            <!-- 表格 -->
            <el-table :data="pageStudents" border style="width: 100%" size="mini">
              <el-table-column type="selection"> </el-table-column>
              <el-table-column type="index" label="序号" width="60" align="center"> </el-table-column>
              <el-table-column prop="student_id" label="学号" width="80" align="center"> </el-table-column>
              <el-table-column prop="name" label="姓名" width="80" align="center"> </el-table-column>
              <el-table-column prop="gender" label="性别" width="60" align="center"> </el-table-column>
              <el-table-column prop="birthday" label="出生日期" width="100" align="center"> </el-table-column>
              <el-table-column prop="mobile" label="电话" width="120" align="center"> </el-table-column>
              <el-table-column prop="email" label="邮箱" width="220" align="center"> </el-table-column>
              <el-table-column prop="address" label="地址" align="center"> </el-table-column>
              <el-table-column label="操作" width="140" align="center">
                <el-button type="success" icon="el-icon-check" size="mini" circle></el-button>
                <el-button type="primary" icon="el-icon-edit" size="mini" circle></el-button>
                <el-button type="danger" icon="el-icon-delete" size="mini" circle></el-button>
              </el-table-column>
            </el-table>
            <!-- 分页 -->
            <el-row style="margin-top: 20px">
              <el-col :span="8" style="text-align: left">
                <el-button type="primary" icon="el-icon-delete" size="mini">批量删除</el-button>
              </el-col>
              <el-col :span="16" style="text-align: right">
                <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                  :current-page="currentpage" :page-sizes="[5, 10, 50, 100]" :page-size="pagesize"
                  layout="total, sizes, prev, pager, next, jumper" :total="total">
                </el-pagination>
              </el-col>
            </el-row>
          </el-main>
          <el-footer style="height: 30px">版权所有：pku-sewm</el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data: function () {
    return {
      students: [], // 所有学生信息
      pageStudents: [], // 当前页的学生信息
      baseURL: 'http://127.0.0.1:8000/api/',
      total: 100, // 数据的总行数
      currentpage: 1, // 当前所在的页
      pagesize: 10
    }
  },
  mounted () {
    // 自动加载数据
    this.getStudents()
  },
  methods: {
    // 获取所有学生信息
    getStudents: function () {
      let that = this
      // 使用Axios
      axios.get(that.baseURL + 'show')
        .then(function (res) {
          // 请求成功后执行的函数
          if (res.data.code === 1) {
            that.students = res.data.data
            // 获取返回记录的总行数
            that.total = res.data.data.length
            // 获取当前页
            that.getPageStudets()
            that.$message({
              message: '数据加载成功！',
              type: 'success'
            })
          } else {
            that.$message.error(res.data.msg)
          }
        })
        .catch(function (err) {
          // 请求失败后执行的函数
          console.log(err)
        })
    },
    // 获取当前页的学生信息
    getPageStudets: function () {
      // 清空pageStudents中的数据
      this.pageStudents = []
      // 获得当前页的数据
      for (let i = (this.currentpage - 1) * this.pagesize; i < this.total; i++) {
        this.pageStudents.push(this.students[i])
        // 判断是否达到一页的要求
        if (this.pageStudents.length === this.pagesize) break
      }
      console.log(this.pageStudents)
    },
    // 分页时修改每页的行数
    handleSizeChange: function (size) {
      this.pagesize = size
      this.getPageStudets()
    },
    // 调整当前的页码
    handleCurrentChange: function (pageNumber) {
      this.currentpage = pageNumber
      this.getPageStudets()
    }
  }
}
</script>

<style>
html,
body,
#app,
.el-container {
  margin: 0px;
  padding: 0px;
  height: 100%;
}
.el-header {
  background-color: #b3c0d1;
  color: #333;
  text-align: left;
  line-height: 80px;
  font-size: 32px;
  font-weight: bold;
}

.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 30px;
  font-size: 14px;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
}
</style>
