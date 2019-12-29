package snake.v1;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.Random;

public class SnakePanel extends JPanel implements KeyListener, ActionListener {

    // 定义七个图片变量，代表七张图片
    private ImageIcon up = new ImageIcon("src/snake/v1/pic/up.png"); // 向上的蛇头
    private ImageIcon down = new ImageIcon("src/snake/v1/pic/down.png"); // 向下的蛇头
    private ImageIcon left = new ImageIcon("src/snake/v1/pic/left.png"); // 向左的蛇头
    private ImageIcon right = new ImageIcon("src/snake/v1/pic/right.png"); // 向右的蛇头
    private ImageIcon food = new ImageIcon("src/snake/v1/pic/food.png");  // 食物
    private ImageIcon body = new ImageIcon("src/snake/v1/pic/body.png");  // 蛇的身体
    private ImageIcon title = new ImageIcon("src/snake/v1/pic/title.jpg"); // 游戏界面的主题

    // 蛇的每一部分
    private int[] snakex = new int[750];
    private int[] snakey = new int[750];

    // 随机生成食物
    private Random rand = new Random();
    private int foodx = rand.nextInt(34) * 25 + 25; //此处的数值根据自己设计的游戏界面的大小来确定
    private int foody = rand.nextInt(24) * 25 + 75;

    // 设置游戏的默认属性
    private int len = 3;
    private int score = 0;
    private String direction = "R"; // U上 D下 L左 R右

    private boolean isStarted = false; // 判断游戏是否开始
    private boolean isFailed = false; // 判断游戏是否结束

    private Timer timer = new Timer(100, this); // 每100毫秒调用一次ActionPerformed

    SnakePanel() { // 建造画布的构造函数
        this.setFocusable(true);  // 获取焦点
        this.addKeyListener(this); // 监听键盘事件
        setup();
        timer.start();
    }

    public void paint(Graphics g) { // Graphics 画笔
        this.setBackground(Color.BLACK); // 设置画布背景颜色
        title.paintIcon(this, g, 25, 11);// 放置主题图片
        g.fillRect(25, 75, 850, 650); // 用画笔设置游戏方框

        // 画蛇头（注意判断蛇头的方向）
        switch (direction) {
            case "R":
                right.paintIcon(this, g, snakex[0], snakey[0]);
                break;
            case "L":
                left.paintIcon(this, g, snakex[0], snakey[0]);
                break;
            case "U":
                up.paintIcon(this, g, snakex[0], snakey[0]);
                break;
            case "D":
                down.paintIcon(this, g, snakex[0], snakey[0]);
                break;
        }

        // 画蛇的身体
        for (int i = 1; i < len; i++)
            body.paintIcon(this, g, snakex[i], snakey[i]);

        // 判断如果游戏没开始显示。。。
        if (!isStarted) {
            g.setColor(Color.WHITE);
            g.setFont(new Font("arial", Font.BOLD, 30));
            g.drawString("Press Space to start / pause", 200, 300);
        }

        // 判断如果游戏结束显示。。。
        if (isFailed) {
            g.setColor(Color.WHITE);
            g.setFont(new Font("arial", Font.BOLD, 30));
            g.drawString("Game Over ! Press space to restart", 200, 300);
        }

        // 显示食物
        food.paintIcon(this, g, foodx, foody);

        // 设置分数和蛇的长度
        g.setColor(Color.WHITE);
        g.setFont(new Font("arial", Font.PLAIN, 15));
        g.drawString("Score : " + score, 650, 37);
        g.drawString("Len :" + len, 650, 57);
    }

    private void setup() { // 游戏初始化
        isStarted = false;
        isFailed = false;
        len = 3;
        score = 0;
        snakex[0] = 100;
        snakex[1] = 75;
        snakex[2] = 50;
        snakey[0] = 100;
        snakey[1] = 100;
        snakey[2] = 100;
    }

    @Override
    public void keyPressed(KeyEvent e) {
        //实现键盘响应
        int KeyCode = e.getKeyCode();
        if (KeyCode == KeyEvent.VK_SPACE) { // 敲击空格现实/消除提示信息
            if (isFailed) {
                //                isStarted = false;  // 可以将这两行放入setup中
                //                isFailed = false;
                setup();
            } else
                isStarted = !isStarted;
        } else if (KeyCode == KeyEvent.VK_UP && !direction.equals("D"))
            direction = "U";
        else if (KeyCode == KeyEvent.VK_DOWN && !direction.equals("U"))
            direction = "D";
        else if (KeyCode == KeyEvent.VK_RIGHT && !direction.equals("L"))
            direction = "R";
        else if (KeyCode == KeyEvent.VK_LEFT && !direction.equals("R"))
            direction = "L";
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        // 1. 再定义一个闹钟
        timer.start();

        // 2. 移动数据
        if (isStarted && !isFailed) {
            // 移动身体
            for (int i = len; i > 0; i--) {
                snakex[i] = snakex[i - 1];
                snakey[i] = snakey[i - 1];
            }

            // 移动头
            switch (direction) {
                case "R":
                    snakex[0] = snakex[0] + 25;
                    if (snakex[0] > 850) snakex[0] = 25;
                    break;
                case "L":
                    snakex[0] = snakex[0] - 25;
                    if (snakex[0] < 25) snakex[0] = 850;
                    break;
                case "U":
                    snakey[0] = snakey[0] - 25;
                    if (snakey[0] < 75) snakey[0] = 650;
                    break;
                case "D":
                    snakey[0] = snakey[0] + 25;
                    if (snakey[0] > 650) snakey[0] = 75;
                    break;
            }

            if (snakex[0] == foodx && snakey[0] == foody) {  // 吃食物
                len++;
                score++;
                foodx = rand.nextInt(34) * 25 + 25;
                foody = rand.nextInt(24) * 25 + 75;
            }

            for (int i = 1; i < len; i++) {  // 如果蛇头碰到自己的身体游戏结束
                if (snakex[0] == snakex[i] && snakey[0] == snakey[i]) {
                    isFailed = true;
                }
            }
        }
        // 3. repaint（）
        repaint();

    }

    @Override
    public void keyTyped(KeyEvent e) {
    }

    @Override
    public void keyReleased(KeyEvent e) {
    }

}
