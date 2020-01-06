package snake.v1;

import javax.swing.*;

public class SankeGame {
    public static void main(String[] args) {
        JFrame frame = new JFrame(); // 创建一个游戏界面的框架
        frame.setBounds(10, 10, 900, 720); // 设置框架的大小
        frame.setResizable(false); // 设置框架大小为不能改变
        // 点击关闭按钮 关闭游戏界面
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        SnakePanel panel = new SnakePanel();  //添加画布
        frame.add(panel); // 刚添加时画布是空的看不到
        frame.setVisible(true); // 允许显示游戏界面
    }
}
