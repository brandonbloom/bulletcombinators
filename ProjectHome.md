A simple Bullet Hell game written in a functional combinator style in Python using pygame.

Here is an example pattern which does a sort of figure-eight out of two octagons. Every time the the bullet moves, it spawns a new bullet which fires off in a straight line.

```
Bullet((400, 300)),
    forever(
        sequence(
            repeat(8,
                sequence(
                    repeat(25, forward(3)),
                    rotate(3.14/4),
                    spawn(forever(forward(2)), color=red))),
            rotate(3.14)))
```

This project is inspired by an article on writing a parser with functional combinators in Arc: <http://awwx.ws/combinator/toc>. I wanted to write something with combinators, but was afraid I wouldn't learn anything blindly copying the parser library. My friend Jace provided this perfect test case while trying to learn F#.