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
                    <el-input v-model="inputstr" placeholder="查询条件" style="width: 360px"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-button-group>
                    <el-button type="primary" icon="el-icon-search" @click="queryStudents">查询</el-button>
                    <el-button type="primary" icon="el-icon-tickets" @click="getAll">全部</el-button>
                    <el-button type="primary" icon="el-icon-circle-plus-outline" @click="addStudent">添加</el-button>
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
            <el-table :data="pageStudents" border style="width: 100%" size="mini"
              @selection-change="handleSelectionChange">>
              <el-table-column type="selection"> </el-table-column>
              <el-table-column type="index" label="序号" width="50" align="center"> </el-table-column>
              <el-table-column prop="student_id" label="学号" width="90" align="center"> </el-table-column>
              <el-table-column prop="name" label="姓名" width="80" align="center"> </el-table-column>
              <el-table-column prop="gender" label="性别" width="60" align="center"> </el-table-column>
              <el-table-column prop="birthday" label="出生日期" width="100" align="center"> </el-table-column>
              <el-table-column prop="mobile" label="电话" width="120" align="center"> </el-table-column>
              <el-table-column prop="email" label="邮箱" width="220" align="center"> </el-table-column>
              <el-table-column prop="address" label="地址" align="center"> </el-table-column>
              <el-table-column label="操作" width="140" align="center">
                <template slot-scope="scope">
                  <el-button type="success" icon="el-icon-more" size="mini" circle @click="viewStudent(scope.row)">
                  </el-button>
                  <el-button type="primary" icon="el-icon-edit" size="mini" circle @click="updateStudent(scope.row)">
                  </el-button>
                  <el-button type="danger" icon="el-icon-delete" size="mini" circle @click="deleteStudent(scope.row)">
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <!-- 分页 -->
            <el-row style="margin-top: 20px">
              <el-col :span="8" style="text-align: left">
                <el-button type="primary" icon="el-icon-delete" size="mini" @click="deleteStudents">批量删除</el-button>
              </el-col>
              <el-col :span="16" style="text-align: right">
                <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                  :current-page="currentpage" :page-sizes="[5, 10, 50, 100]" :page-size="pagesize"
                  layout="total, sizes, prev, pager, next, jumper" :total="total">
                </el-pagination>
              </el-col>
            </el-row>
            <!-- 学生明细弹出框 -->
            <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" :close-on-click-modal="false" width="50%"
              style="text-align: left" @close="closeDialog('studentForm')">
              <!-- 表单 -->
              <el-form :model="studentForm" :rules="rules" :inline="true" size="mini" label-width="110px"
                label-position="right" style="margin-left:20px" ref="studentForm">
                <!-- 上传头像 -->
                <el-upload class="avatar-uploader" :show-file-list="false" :before-upload="beforeAvatarUpload"
                  style="text-align: center; margin: 20px"  :http-request="uploadPicPost" :disabled="isView">
                  <img v-if="studentForm.image" :src="studentForm.imageUrl" class="avatar">
                  <i v-else class="el-icon-plus avatar-uploader-icon" style="line-height: 178px;"></i>
                </el-upload>
                <el-form-item label="学号：" prop="student_id">
                  <el-input :disabled="isEdit||isView" v-model="studentForm.student_id" suffix-icon="el-icon-edit">
                  </el-input>
                </el-form-item>
                <el-form-item label="姓名：" prop="name">
                  <el-input :disabled="isView" v-model="studentForm.name" suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="性别：" prop="gender">
                  <el-select :disabled="isView" v-model="studentForm.gender" placeholder="请选择性别">
                    <el-option label="男" value="男"></el-option>
                    <el-option label="女" value="女"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="出生日期：" prop="birthday">
                  <el-date-picker :disabled="isView" v-model="studentForm.birthday" value-format="yyyy-MM-dd"
                    type="date" placeholder="请选择日期" style="width:93%">
                  </el-date-picker>
                </el-form-item>
                <el-form-item label="手机号码：" prop="mobile">
                  <el-input :disabled="isView" v-model="studentForm.mobile" suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="邮箱地址：" prop="email">
                  <el-input :disabled="isView" v-model="studentForm.email" suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <div>
                  <el-form-item :span="24" label="家庭住址：" prop="address">
                    <el-input :disabled="isView" v-model="studentForm.address" suffix-icon="el-icon-edit"
                      style="width:272%"></el-input>
                  </el-form-item>
                </div>
              </el-form>
              <span slot="footer" class="dialog-footer" v-show="!isView">
                <el-button type="primary" size="mini" @click="submitStudentForm('studentForm')">确 定</el-button>
                <el-button type="info" size="mini" @click="closeDialog('studentForm')">取 消</el-button>
              </span>
            </el-dialog>
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
    // 校验学号是否存在
    const checkStudentId = (rule, value, callback) => {
      if (this.isEdit) {
        callback()
      }
      axios.post(this.baseURL + 'api/checkID', { student_id: value })
        .then((res) => {
          if (res.data.code === 1) {
            // 请求成功
            if (res.data.existed) {
              callback(new Error('学号已存在'))
            } else {
              callback()
            }
          } else {
            // 请求失败
            callback(new Error('后端出现异常'))
          }
        })
        .catch((err) => {
          console.log(err)
        })
    }

    return {
      students: [], // 所有学生信息
      pageStudents: [], // 当前页的学生信息
      baseURL: 'http://127.0.0.1:2020/',
      inputstr: '',
      selectStudents: [],
      total: 100, // 数据的总行数
      currentpage: 1, // 当前所在的页
      pagesize: 10,
      dialogVisible: false,
      dialogTitle: '',
      isView: false,
      isEdit: false,
      studentForm: {
        student_id: '',
        name: '',
        gender: '',
        birthday: '',
        mobile: '',
        email: '',
        address: '',
        image: '',
        imageUrl: ''
      },
      rules: {
        student_id: [
          { required: true, message: '学号不能为空', trigger: 'blur' },
          { pattern: /^[9][5]\d{3}$/, message: '学号必须是95xxx', trigger: 'blur' },
          { validator: checkStudentId, trigger: 'blur' }
        ],
        name: [
          { required: true, message: '姓名不能为空', trigger: 'blur' },
          { pattern: /^[\u4e00-\u9fa5]{2,5}$/, message: '姓名必须是2-5个汉字', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '性别不能为空', trigger: 'change' }
        ],
        birthday: [
          { required: true, message: '出生日期不能为空', trigger: 'change' }
        ],
        mobile: [
          { required: true, message: '手机号码不能为空', trigger: 'blur' },
          { pattern: /^[1][35789]\d{9}$/, message: '手机号码需要符合规范', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '邮箱地址不能为空', trigger: 'blur' },
          { pattern: /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/, message: '邮箱地址需要符合规范', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '家庭地址不能为空', trigger: 'blur' }
        ]
      }
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
      axios.get(that.baseURL + 'api/show')
        .then(function (res) {
          // 请求成功后执行的函数
          if (res.data.code === 1) {
            that.students = res.data.data
            // 获取返回记录的总行数
            that.total = res.data.data.length
            // 获取当前页
            that.getPageStudets()
            that.$message({
              message: '全部数据加载成功！',
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
    // 全部按钮的回调函数
    getAll: function () {
      this.inputstr = ''
      this.getStudents()
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
    // 实现学生信息查询
    queryStudents: function () {
      let that = this
      axios.post(that.baseURL + 'api/query', { inputstr: that.inputstr })
        .then(function (res) {
          if (res.data.code === 1) {
            that.students = res.data.data
            // 获取返回记录的总行数
            that.total = res.data.data.length
            // 获取当前页
            that.getPageStudets()
            that.$message({
              message: '查询成功！',
              type: 'success'
            })
          } else {
            that.$message.error(res.data.msg)
          }
        })
        .catch(function (err) {
          console.length(err)
          that.$message.error('获取后端查询结果出现异常！')
        })
    },
    // 添加学生时打开对话框
    addStudent: function () {
      this.dialogTitle = '添加学生明细'
      this.dialogVisible = true
    },
    // 根据学号获取图片
    getImageByID (id) {
      for (const oneStudent of this.students) {
        if (oneStudent.student_id === id) return oneStudent.image
      }
    },
    // 查看学生的明细
    viewStudent: function (row) {
      this.dialogTitle = '查看学生明细'
      this.isView = true
      this.dialogVisible = true
      this.studentForm = JSON.parse(JSON.stringify(row))
      this.studentForm.image = this.getImageByID(row.student_id)
      this.studentForm.imageUrl = this.baseURL + 'media/' + this.studentForm.image
    },
    updateStudent: function (row) {
      this.dialogTitle = '修改学生明细'
      this.isEdit = true
      this.dialogVisible = true
      this.studentForm = JSON.parse(JSON.stringify(row))
      this.studentForm.image = this.getImageByID(row.student_id)
      this.studentForm.imageUrl = this.baseURL + 'media/' + this.studentForm.image
    },
    // 关闭弹出框
    closeDialog: function (formName) {
      this.dialogVisible = false
      this.$refs[formName].resetFields()
      this.isView = false
      this.isEdit = false
      this.studentForm.student_id = ''
      this.studentForm.name = ''
      this.studentForm.gender = ''
      this.studentForm.birthday = ''
      this.studentForm.mobile = ''
      this.studentForm.email = ''
      this.studentForm.address = ''
      this.studentForm.image = ''
      this.studentForm.imageUrl = ''
    },
    // 提交表单
    submitStudentForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // 校验成功
          console.log(this.isEdit)
          if (this.isEdit) {
            // 修改
            this.submitUpdateStudent()
          } else {
            // 添加
            this.submitAddStudent()
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 提交表单，添加学生到数据库
    submitAddStudent () {
      let that = this
      axios.post(that.baseURL + 'api/add', that.studentForm)
        .then((res) => {
          // 执行成功
          if (res.data.code === 1) {
            that.students = res.data.data
            // 获取返回记录的总行数
            that.total = res.data.data.length
            // 获取当前页
            that.getPageStudets()
            that.$message({
              message: '数据添加成功！',
              type: 'success'
            })
            // 关闭窗体
            that.closeDialog('studentForm')
          } else {
            that.$message.error(res.data.msg)
          }
        })
        .catch((err) => {
          // 执行失败
          console.log(err)
          that.$message.error('获取后端查询结果出现异常！')
        })
    },
    // 提交表单，修改学生信息
    submitUpdateStudent () {
      let that = this
      axios.post(that.baseURL + 'api/update', that.studentForm)
        .then((res) => {
          // 执行成功
          if (res.data.code === 1) {
            that.students = res.data.data
            // 获取返回记录的总行数
            that.total = res.data.data.length
            // 获取当前页
            that.getPageStudets()
            that.$message({
              message: '数据修改成功！',
              type: 'success'
            })
            // 关闭窗体
            that.closeDialog('studentForm')
          } else {
            that.$message.error(res.data.msg)
          }
        })
        .catch((err) => {
          // 执行失败
          console.log(err)
          that.$message.error('修改时获取后端查询结果出现异常！')
        })
    },
    // 删除一条学生的记录
    deleteStudent (row) {
      // 提示用户确认
      this.$confirm('此操作将永久删除该学生信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let that = this
        axios.post(that.baseURL + 'api/delete', { student_id: row.student_id })
          .then(res => {
            if (res.data.code === 1) {
              that.students = res.data.data
              that.total = res.data.data.length
              that.getPageStudets()
              that.$message({
                type: 'success',
                message: '删除成功!'
              })
            } else {
              that.$message.error(res.data.msg)
            }
          })
          .catch(err => {
            console.log(err)
            that.$message.error('删除时获取后端查询结果出现异常！')
          })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 批量删除
    deleteStudents () {
      // 提示用户确认
      this.$confirm('此操作将永久删除' + this.selectStudents.length + '个学生信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let that = this
        axios.post(that.baseURL + 'api/deletebatch', { student: that.selectStudents })
          .then(res => {
            if (res.data.code === 1) {
              that.students = res.data.data
              that.total = res.data.data.length
              that.getPageStudets()
              that.$message({
                type: 'success',
                message: '批量删除成功!'
              })
            } else {
              that.$message.error(res.data.msg)
            }
          })
          .catch(err => {
            console.log(err)
            that.$message.error('批量删除时获取后端查询结果出现异常！')
          })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
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
    },
    // 选择复选框触发的操作
    handleSelectionChange (data) {
      console.log(data)
      this.selectStudents = data
    },
    // 上传头像
    uploadPicPost (file) {
      let that = this
      let fileReq = new FormData()
      fileReq.append('avatar', file.file)
      axios({
        method: 'post',
        url: that.baseURL + 'api/upload',
        data: fileReq
      })
        .then(res => {
          if (res.data.code === 1) {
            that.studentForm.image = res.data.name
            that.studentForm.imageUrl = that.baseURL + 'media/' + res.data.name
          } else {
            that.$message.error(res.data.msg)
          }
        })
        .catch(err => {
          console.log(err)
          that.$message.error('上传头像出现异常')
        })
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

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 120px;
  height: 160px;
  display: block;
}
</style>
