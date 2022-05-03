# iNeuronsControllerPy

## 開發文件
  - [Google Doc](https://docs.google.com/document/d/1HhIDl97UI30qQpnuf0UWvTpVVOCZouWq4llGl8MKFRI/edit?usp=sharing)

## 分支說明
  - develop/1.x : 原 develop 分支
  - develop/2.x : 由 `1.3.2` 切出、Controller 專案打包
  - fn-Controller 所有 controller 功能都要合併到此 `./controller.py`
    - test-Controller 以 pytest 針對 fn_Controller 做單元測試
    - uml 類別圖、功能說明示意圖
    - fn-ControllerPackage `./__init__.py`
      - fn-ControllerWebApp `ctrl_app/controller/__init__.py` 
        - web Django