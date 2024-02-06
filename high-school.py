from manim import *
from math import log10 , floor , sqrt , exp , gcd
import numpy as np
import colorsys
import itertools
from scipy.optimize import fsolve

# RED = RED_B

myTemplate = TexTemplate()

def color_text(r_list, g_list, y_list, b_list, formula):
    for i,j,k in r_list:
        for l in range(k):
            formula[i][j+l].set_color(RED)
    for i,j,k in g_list:
        for l in range(k):
            formula[i][j+l].set_color(GREEN)
    for i,j,k in y_list:
        for l in range(k):
            formula[i][j+l].set_color(YELLOW)
    for i,j,k in b_list:
        for l in range(k):
            formula[i][j+l].set_color(BLUE)

def color_cell_text(r_list, g_list, y_list, b_list, formula):
    for i,j,k in r_list:
        for l in range(k):
            formula[i][0][j+l].set_color(RED)
    for i,j,k in g_list:
        for l in range(k):
            formula[i][0][j+l].set_color(GREEN)
    for i,j,k in y_list:
        for l in range(k):
            formula[i][0][j+l].set_color(YELLOW)
    for i,j,k in b_list:
        for l in range(k):
            formula[i][0][j+l].set_color(BLUE)

def color_table(r_list, g_list, y_list, b_list, formula):
    formula_collection = formula[0]
    return color_cell_text(r_list, g_list, y_list, b_list, formula_collection)

def ingredient_recipe(matrix, vector):

            matrix_copy = matrix.copy()
            vector_copy = vector.copy()
            vector_copy.next_to(matrix_copy, RIGHT)

            curr_tex = VGroup(matrix_copy, vector_copy)
            equals = MathTex(r"=").next_to(curr_tex)
            curr_tex = VGroup(*curr_tex, equals)

            for i in range(len(vector_copy[0])):
                
                if i:
                    plus = MathTex(r"+").next_to(curr_tex)
                    curr_tex = VGroup(*curr_tex, plus)

                recipe_i = vector_copy.get_rows()[i].copy().next_to(curr_tex, RIGHT)
                left_bracket_i = matrix_copy[1].copy().next_to(recipe_i, RIGHT)
                ingredient_i = matrix_copy.get_columns()[i].copy().next_to(left_bracket_i , RIGHT)
                right_bracket_i = matrix_copy[2].copy().next_to(ingredient_i, RIGHT)


                curr_tex = VGroup(*curr_tex, recipe_i, left_bracket_i, ingredient_i, right_bracket_i)
            
            curr_tex.move_to(ORIGIN)

            return curr_tex

def add_brackets(mobj):
    bracket_pair = Tex("\\big(", "\\big)")
    bracket_pair.scale(2)
    bracket_pair.stretch_to_fit_height(
        mobj.get_height() + 2 * 0.1
    )
    l_bracket, r_bracket = bracket_pair.split()
    l_bracket.next_to(mobj, LEFT, .2)
    r_bracket.next_to(mobj, RIGHT, .2)
    return VGroup(l_bracket, mobj, r_bracket)

#Font Packages
def template_additions(tex_template):
    tex_template.add_to_preamble(r"\usepackage{amsmath}  \usepackage{amssymb} \usepackage{ragged2e} \usepackage{cancel}")
    tex_template.add_to_preamble(r"\usepackage{mathtools}")
    #Math Notation
    tex_template.add_to_preamble(r"\newcommand{\dpdt}[2]{#1 \cdot #2}")
    tex_template.add_to_preamble(r"\newcommand{\cross}{\times}")
    tex_template.add_to_preamble(r"\newcommand{\cpdt}[2]{#1 \cross #2}")
    tex_template.add_to_preamble(r"\newcommand{\To}{\Rightarrow}")
    tex_template.add_to_preamble(r"\newcommand{\paren}[1]{\left( #1 \right)}")
    tex_template.add_to_preamble(r"\newcommand{\parenb}[1]{\left[ #1 \right]}")
    tex_template.add_to_preamble(r"\newcommand{\parenl}[1]{\left| #1 \right|}")
    tex_template.add_to_preamble(r"\newcommand{\mat}[1]{\begin{matrix}#1\end{matrix}}")
    tex_template.add_to_preamble(r"\newcommand{\pmat}[1]{\paren{\begin{matrix}#1\end{matrix}}}")
    tex_template.add_to_preamble(r"\newcommand{\dmat}[1]{\parenl{\begin{matrix}#1\end{matrix}}}")
    tex_template.add_to_preamble(r"\newcommand{\dsfrac}[2]{{\displaystyle \frac{#1}{#2}}}")
    tex_template.add_to_preamble(r"\newcommand{\sett}[1]{\left\{{#1}\right\}}")

    #Calculus
    tex_template.add_to_preamble(r"\newcommand{\diff}{\mathrm{d}}")
    tex_template.add_to_preamble(r"\newcommand{\del}{\partial}")
    tex_template.add_to_preamble(r"\newcommand{\deriv}[2]{\dsfrac{\mathrm{d} #1}{\mathrm{d}#2}}")
    tex_template.add_to_preamble(r"\newcommand{\nderiv}[3]{\dsfrac{\mathrm{d}^{#3} #1}{\mathrm{d}#2^{#3}}}")
    tex_template.add_to_preamble(r"\newcommand{\pderiv}[2]{\dsfrac{\del #1}{\del #2}}")
    tex_template.add_to_preamble(r"\newcommand{\rint}[4]{\int_{#1}^{#2} #3\ \diff{#4}}")

    #Boldface Vectors
    tex_template.add_to_preamble(r"\newcommand{\myvec}[1]{\mathbf{#1}}")
    tex_template.add_to_preamble(r"\newcommand{\avec}{\myvec{a}}")
    tex_template.add_to_preamble(r"\newcommand{\bvec}{\myvec{b}}")
    tex_template.add_to_preamble(r"\newcommand{\cvec}{\myvec{c}}")
    tex_template.add_to_preamble(r"\newcommand{\dvec}{\myvec{d}}")
    tex_template.add_to_preamble(r"\newcommand{\evec}{\myvec{e}}")
    tex_template.add_to_preamble(r"\newcommand{\ivec}{\myvec{i}}")
    tex_template.add_to_preamble(r"\newcommand{\jvec}{\myvec{j}}")
    tex_template.add_to_preamble(r"\newcommand{\kvec}{\myvec{k}}")
    tex_template.add_to_preamble(r"\newcommand{\mvec}{\myvec{m}}")
    tex_template.add_to_preamble(r"\newcommand{\nvec}{\myvec{n}}")
    tex_template.add_to_preamble(r"\newcommand{\ovec}{\myvec{0}}")
    tex_template.add_to_preamble(r"\newcommand{\pvec}{\myvec{p}}")
    tex_template.add_to_preamble(r"\newcommand{\qvec}{\myvec{q}}")
    tex_template.add_to_preamble(r"\newcommand{\rvec}{\myvec{r}}")
    tex_template.add_to_preamble(r"\newcommand{\svec}{\myvec{s}}")
    tex_template.add_to_preamble(r"\newcommand{\tvec}{\myvec{t}}")
    tex_template.add_to_preamble(r"\newcommand{\uvec}{\myvec{u}}")
    tex_template.add_to_preamble(r"\newcommand{\vvec}{\myvec{v}}")
    tex_template.add_to_preamble(r"\newcommand{\wvec}{\myvec{w}}")
    tex_template.add_to_preamble(r"\newcommand{\xvec}{\myvec{x}}")
    tex_template.add_to_preamble(r"\newcommand{\yvec}{\myvec{y}}")
    tex_template.add_to_preamble(r"\newcommand{\zvec}{\myvec{z}}")


    tex_template.add_to_preamble(r"\newcommand{\Avec}[1]{\overrightarrow{#1}}")

    #TikZ
    tex_template.add_to_preamble(r"\usepackage{tikz}")

    #Coordinate Vectors
    tex_template.add_to_preamble(r"\newcommand{\vecnoo}[3]{\pmat{#1 \\ #2 \\ #3}}")

    #Blackboard Letters
    tex_template.add_to_preamble(r"\newcommand{\blackboard}[1]{\mathbb{#1}}")
    tex_template.add_to_preamble(r"\newcommand{\NN}{\blackboard{N}}")
    tex_template.add_to_preamble(r"\newcommand{\ZZ}{\blackboard{Z}}")
    tex_template.add_to_preamble(r"\newcommand{\QQ}{\blackboard{Q}}")
    tex_template.add_to_preamble(r"\newcommand{\RR}{\blackboard{R}}")
    tex_template.add_to_preamble(r"\newcommand{\CC}{\blackboard{C}}")
    tex_template.add_to_preamble(r"\newcommand{\EE}{\blackboard{E}}")
    tex_template.add_to_preamble(r"\newcommand{\PP}{\blackboard{P}}")
    tex_template.add_to_preamble(r"\newcommand{\VV}{\mathrm{Var}}")
    
    tex_template.add_to_preamble(r"\newcommand{\eeps}{\varepsilon}")

    #H2 Math
    tex_template.add_to_preamble(r"\newcommand{\func}[1]{\textsf{#1}}")
    tex_template.add_to_preamble(r"\newcommand{\dom}[1]{\mathrm{D}_{#1}}")
    tex_template.add_to_preamble(r"\newcommand{\range}[1]{\mathrm{R}_{#1}}")
    tex_template.add_to_preamble(r"\renewcommand{\geq}{\geqslant}")
    tex_template.add_to_preamble(r"\renewcommand{\leq}{\leqslant}")
    tex_template.add_to_preamble(r"\newcommand{\inv}[1]{#1^{-1}}")
    tex_template.add_to_preamble(r"\newcommand{\imu}{i}")
    tex_template.add_to_preamble(r"\newcommand{\Prob}{\PP}")

    tex_template.add_to_preamble(r"\newcommand{\CProb}[2]{\Prob(#1 \mid #2)}")

    tex_template.add_to_preamble(r"\newcommand{\Var}{\mathrm{Var}}")
    tex_template.add_to_preamble(r"\newcommand{\Iff}{\Longleftrightarrow}")
    tex_template.add_to_preamble(r"\newcommand{\BPI}[1]{\underbracket{\phantom- #1 \phantom-}_{\text I}}")
    tex_template.add_to_preamble(r"\newcommand{\BPS}[1]{\underbracket{\phantom- #1 \phantom-}_{\text S}}")
    tex_template.add_to_preamble(r"\newcommand{\BPD}[1]{\underbracket{\phantom- #1 \phantom-}_{\text D}}")
    tex_template.add_to_preamble(r"\newcommand{\BPF}[2]{\underbracket{\phantom{--} #1 \phantom{--}}_{#2}}")

    tex_template.add_to_preamble(r"\newcommand{\tsum}{{\textstyle \sum}}")
    tex_template.add_to_preamble(r"\newcommand{\Hnull}{\mathrm{H}_0}")
    tex_template.add_to_preamble(r"\newcommand{\Halt}{\mathrm{H}_1}")
    
    tex_template.add_to_preamble(r"\newcommand{\tou}[1]{\xrightarrow{#1}}")
    tex_template.add_to_preamble(r"\newcommand{\sdiff}[2]{{#1} \backslash {#2}}")
    tex_template.add_to_preamble(r"\newcommand{\indep}{\perp \!\!\! \perp}")
    tex_template.add_to_preamble(r"\newcommand{\II}{\mathbb{I}}")
    
    #Calligraphic Letters
    tex_template.add_to_preamble(r"\newcommand{\ccal}[1]{\mathcal{#1}}")

    tex_template.add_to_preamble(r"\newcommand{\intparts}[3]{\underbracket{\phantom{-}#1\phantom{-}}_{\func I} \underbracket{\phantom{-}#2\phantom{-}}_{\func S} - \rint{}{}{\underbracket{\phantom{-}#1\phantom{-}}_{\func I}\underbracket{\phantom{-}#3\phantom{-}}_{\func D}}{x}}")

    tex_template.add_to_preamble(r"\usepackage{setspace}")
    tex_template.add_to_preamble(r"\setstretch{1.25}")

template_additions(myTemplate)

class WarningSign(Scene):

    def construct(self):
        # Create a triangular warning sign
        warning_sign = self.create_warning_sign()

        # Create an exclamation mark
        exclamation_mark = self.create_exclamation_mark()

        # Group the warning sign and the exclamation mark
        warning_group = VGroup(warning_sign, exclamation_mark)

        # Position the warning group in the center of the screen
        warning_group.move_to(ORIGIN)

        return warning_group

    def create_warning_sign(self):
        # Create a triangular shape with rounded vertices
        warning_sign = Triangle(
            fill_color=PURE_RED,
            fill_opacity=.8,
            stroke_color=WHITE,
            stroke_width=5,
        )
        warning_sign.set_height(2)
        warning_sign.set_width(2)
        warning_sign.round_corners(0.1)  # Set corner radius

        return warning_sign

    def create_exclamation_mark(self):
        # Create an exclamation mark using Text
        exclamation_mark = Tex(r"\textbf{!}", font_size=48, color=WHITE).scale(2)

        return exclamation_mark

class Intro(MovingCameraScene):

    def construct(self):

        self.camera.frame.scale(1.25)

        warning_sign = MathTex(r"f(x)")
        warning_sign[0][2].set_color(YELLOW)
        
        warning_tex = MathTex(r"\times\ \! 20").set_color(YELLOW).scale(1.2).next_to(warning_sign, RIGHT)

        func_list = MathTex(r"1. \quad & \text{$f(x) = mx + c$}\\ ",
                            r"2. \quad & \text{$f(x) = ax^2 + bx + c$}\\ ",
                            r"3. \quad & \text{$f(x) = a_3x^3 + a_2x^2 + a_1x + a_0$}\\ ",
                            r"4. \quad & \text{$f(x) = 1/x^n$}\\ ",
                            r"5. \quad & \text{$f(x) = \sqrt{x}$}\\ ",
                            r"6. \quad & \text{$f(x) = \sqrt[n]{x}$}\\ ",
                            r"7. \quad & \text{$f(t) = A\sin(\omega t + \varphi)$}\\ ",
                            r"8. \quad & \text{$f(t) = A\cos(\omega t + \varphi)$}\\ ",
                            r"9. \quad & \text{$f(\theta) = \tan(\theta)$}\\ ",
                            r"10. \quad & \text{Periodic function}\\ ",
                            r"11. \quad & \text{$f(\theta) = \cot(\theta)$}\\ ",
                            r"12. \quad & \text{$f(\theta) = \csc(\theta)$}\\ ",
                            r"13. \quad & \text{$f(\theta) = \sec(\theta)$}\\ ",
                            r"14. \quad & \text{$f(t) = f(0) e^{kt}$}\\ ",
                            r"15. \quad & \text{$f(t) = f(0) e^{-kt}$}\\ ",
                            r"16. \quad & \text{$f(t) = f(0) a^t$}\\ ",
                            r"17. \quad & \text{$f(x) = \ln(x - c)$}\\ ",
                            r"18. \quad & \text{$f(x) = \log_a(x - c)$}\\ ",
                            r"19. \quad & \text{$f(x) = |x|$}\\ ",
                            r"20. \quad & \text{Piecewise function}\\ ",
                            tex_template = myTemplate)
        
        func_list.scale(.7)

        for i in range(len(func_list)):

            if i < 9:

                func_list[i][4].set_color(YELLOW)
            
            if i >= 10 and i < 19:

                func_list[i][5].set_color(YELLOW)

        color_text(r_list = [(0, 7, 1), 
                             (1, 7, 1), (6, 7, 1), (7, 7, 1), 
                             (13, 13, 1), (14, 14, 1), 
                             (15, 12, 1), (17, 11, 1), ],
                   g_list = [(0, 10, 1), (1, 14, 1), 
                             (6, 15, 1), (7, 15, 1), 
                             (13, 10, 1), (14, 10, 1), 
                             (15, 10, 1), ],
                   y_list = [(0, 8, 1),
                             (1, 8, 1), (1, 12, 1), (2, 9, 1), (2, 14, 1), (2, 19, 1), 
                             (3, 9, 1), (4, 9, 1), (5, 10, 1), 
                             (6, 13, 1), (7, 13, 1), (8, 11, 1), 
                             (10, 12, 1), (11, 12, 1), (12, 12, 1), 
                             (13, 14, 1), (14, 15, 1), 
                             (15, 13, 1), 
                             (16, 11, 1), 
                             (17, 13, 1), (18, 9, 1), ],
                   b_list = [(1, 11, 1), (2, 7, 2), (2, 12, 2), (2, 17, 2), (2, 21, 2), 
                             (3, 10, 1), (5, 7, 1), (6, 12, 1), (7, 12, 1), 
                             (16, 13, 1), (17, 15, 1), ],
                   formula = func_list)

        func_list[10:].next_to(func_list[:10], RIGHT, buff = 1)

        VGroup(warning_sign, warning_tex).scale(2.3).next_to(func_list, UP, buff = 1)
        VGroup(warning_sign, warning_tex, func_list).move_to(ORIGIN)

        self.play(Write(VGroup(warning_sign, warning_tex)), run_time = 1.5)
        self.play(Write(func_list), run_time = 6)
        self.wait(5)

    pass

### Functions to plot

### ALGEBRAIC

class Linear(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{1.\ \text{Linear graph}}").scale(1.2).next_to(header_position, RIGHT)

        math_def = MathTex(r"f(x) &= mx + c\\ ",
                           r"m &= ", r"-0.50\\ ",
                           r"c &= ", r"-1.00\\ ",
                           tex_template = myTemplate)
        
        color_text(r_list = [(0, 5, 1), (1, 0, 1), ],
                   g_list = [(0, 8, 1), (3, 0, 1), ],
                   y_list = [(0, 2, 1), (0, 6, 1),],
                   b_list = [],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{Gradient: $m$}\\ ",
                                r"2.\quad & \text{$y$-intercept: $(0, c)$}\\ ",
                                r"3.\quad & \text{Speed of an object}\\ ",
                                r"4.\quad & \text{$f(x) = f(t) + m(x - t)$}\\ ",
                                r"5.\quad & \text{Calculus approximations}\\ ",
                                tex_template = myTemplate).scale(.9)
        
        color_text(r_list = [(0, -1, 1), (3, 12, 1), ],
                   g_list = [(1, -2, 1), (3, 9, 1), (3, 16, 1), ],
                   y_list = [(1, 2, 1), (3, 4, 1), (3, 14, 1), ],
                   b_list = [],
                   formula = math_implications)
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-2.3, 2.3],
            y_range=[-2.3, 2.3],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"x").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        line_gradient = ValueTracker(1)
        line_intercept = ValueTracker(0)

        gradient_tex = always_redraw(lambda : MathTex(round(line_gradient.get_value(), 2)).move_to(math_def[2]).set_color(RED))
        intercept_tex = always_redraw(lambda : MathTex(round(line_intercept.get_value(), 2)).move_to(math_def[4]).set_color(GREEN))

        def func_1(grad, intercept):

            return lambda x : grad * x + intercept

        graph_pic = always_redraw(lambda : ax.plot(func_1(line_gradient.get_value(), line_intercept.get_value()), x_range=[-2.2, 2.2, 0.01], color=YELLOW).set_z_index(-1))

        def graph_label_imp(gradient, intercept, input):

            curr_tex = MathTex(r"y = f(x)").next_to(ax.c2p(input, func_1(gradient, intercept)(input), 0), UP)
            curr_tex[0][0].set_color(YELLOW)
            curr_tex[0][4].set_color(YELLOW)

            return curr_tex
        
        graph_label = always_redraw(lambda : graph_label_imp(line_gradient.get_value(), line_intercept.get_value(), 2.2))

        color_text(y_list = [(0, 0, 1), (0, 4, 1), ],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_pic, graph_label
               ).move_to(diagram_position.get_center())
        
        self.play(Write(header))
        self.wait()
        
        self.play(Write(math_def[0]))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()

        self.play(Write(math_def[1]))
        self.play(Write(gradient_tex))
        self.wait()

        self.play(Write(math_def[3]))
        self.play(Write(intercept_tex))
        self.wait()

        self.play(line_gradient.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(line_gradient.animate.set_value(0), run_time = 3)
        self.wait()
        self.play(line_gradient.animate.set_value(-.5), run_time = 3)
        self.wait()

        self.play(Write(math_implications[0]), run_time = 2)
        self.wait()
        self.play(line_gradient.animate.set_value(.5), run_time = 3)
        self.wait()

        def intercept_dot(curr_int):

            geometric_dot = Dot().move_to(ax.c2p(0, curr_int, 0))

            dot_label = MathTex(r"(0,", round(curr_int, 2), r")").next_to(geometric_dot, UL, buff = .1)
            dot_label[1].set_color(GREEN)

            return VGroup(geometric_dot, dot_label)
        
        moving_intercept = always_redraw(lambda : intercept_dot(line_intercept.get_value()))

        self.play(Write(moving_intercept))
        self.wait()

        self.play(line_intercept.animate.set_value(-1), run_time = 3)
        self.wait()
        self.play(line_intercept.animate.set_value(1), run_time = 3)
        self.wait()
        self.play(Write(math_implications[1]), run_time = 2)
        self.wait()
        
        for k in range(2, len(math_implications)):

            self.play(Write(math_implications[k]), run_time = 2)
            self.wait()
        
        self.wait(5)

        pass

    pass

class Quadratic(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{2.\ \text{Quadratic graph}}").scale(1.2).next_to(header_position, RIGHT)

        math_def = MathTex(r"f(x) &= ax^2 + bx + c\\ ",
                           r"a &= ", r"-0.50\\ ",
                           r"b &= ", r"-1.00\\ ",
                           r"c &= ", r"-1.00\\ ",
                           tex_template = myTemplate)
        
        color_text(r_list = [(0, 5, 1), (1, 0, 1), ],
                   g_list = [(0, 12, 1), (5, 0, 1), ],
                   y_list = [(0, 2, 1), (0, 6, 1), (0, 10, 1), ],
                   b_list = [(0, 9, 1), (3, 0, 1), ],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{$y$-intercept: $(0, c)$}\\ ",
                                r"2.\quad & \text{Turning point: $(h, k)$}\\ ",
                                r"3.\quad & \text{Distance travelled}\\ ",
                                r"4.\quad & \text{Quadratic forms}\\ ",
                                tex_template = myTemplate).scale(.9)
        
        color_text(r_list = [],
                   g_list = [(0, -2, 1), ],
                   y_list = [(0, 2, 1), ],
                   b_list = [(1, -2, 1), (1, -4, 1), ],
                   formula = math_implications)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-2.3, 2.3],
            y_range=[-10, 10],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"x").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        parabola_a = ValueTracker(1)
        parabola_b = ValueTracker(0)
        parabola_c = ValueTracker(0)

        parabola_a_tex = always_redraw(lambda : MathTex(round(parabola_a.get_value(), 2)).move_to(math_def[2]).set_color(RED))
        parabola_b_tex = always_redraw(lambda : MathTex(round(parabola_b.get_value(), 2)).move_to(math_def[4]).set_color(BLUE))
        parabola_c_tex = always_redraw(lambda : MathTex(round(parabola_c.get_value(), 2)).move_to(math_def[6]).set_color(GREEN))

        def func_1(parab_a, parab_b, parab_c):

            return lambda x : parab_a * (x ** 2) + parab_b * x + parab_c

        graph_pic = always_redraw(lambda : ax.plot(func_1(parabola_a.get_value(), parabola_b.get_value(), parabola_c.get_value()), x_range=[-2.2, 2.2, 0.01], color=YELLOW).set_z_index(-1))

        def graph_label_imp(parab_a, parab_b, parab_c, input_val):

            curr_tex = MathTex(r"y = f(x)").next_to(ax.c2p(2.2, func_1(parab_a, parab_b, parab_c)(input_val), 0), UP)

            for i in [0, 4]:
                curr_tex[0][i].set_color(YELLOW)

            return curr_tex

        graph_label = always_redraw(lambda : graph_label_imp(parabola_a.get_value(), parabola_b.get_value(), parabola_c.get_value(), 2.2))

        color_text(y_list = [],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_pic, graph_label
               ).move_to(diagram_position.get_center())
        
        self.play(Write(header))
        self.wait()
        
        self.play(Write(math_def[0]))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()

        self.play(Write(math_def[1]))
        self.play(Write(parabola_a_tex))
        self.wait()

        self.play(Write(math_def[3]))
        self.play(Write(parabola_b_tex))
        self.wait()

        self.play(Write(math_def[5]))
        self.play(Write(parabola_c_tex))
        self.wait()

        self.play(parabola_a.animate.set_value(1.8), run_time = 3)
        self.wait()
        self.play(parabola_a.animate.set_value(0), run_time = 3)
        self.wait()
        self.play(parabola_a.animate.set_value(-1.8), run_time = 3)
        self.wait()
        self.play(parabola_a.animate.set_value(1), run_time = 3)
        self.wait()


        self.play(parabola_b.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(parabola_b.animate.set_value(0), run_time = 3)
        self.wait()
        self.play(parabola_b.animate.set_value(-2), run_time = 3)
        self.wait()
        self.play(parabola_b.animate.set_value(-1), run_time = 3)
        self.wait()

        def intercept_dot(curr_int):

            geometric_dot = Dot().move_to(ax.c2p(0, curr_int, 0))

            dot_label = MathTex(r"(0,", round(curr_int, 2), r")").next_to(geometric_dot, DL, buff = .1)

            dot_label[1].set_color(GREEN)

            return VGroup(geometric_dot, dot_label)
        
        moving_intercept = always_redraw(lambda : intercept_dot(parabola_c.get_value()))

        self.play(Write(moving_intercept))
        self.wait()

        self.play(parabola_c.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(parabola_c.animate.set_value(-8), run_time = 3)
        self.wait()
        self.play(parabola_c.animate.set_value(-2), run_time = 3)
        self.wait()

        ### math-implications

        self.play(Write(math_implications[0]), run_time = 2)
        self.wait()

        def turning_point_dot(parab_a, parab_b, parab_c):

            curr_input = -parab_b/(2 * parab_a)

            geometric_dot = Dot().move_to(ax.c2p(curr_input, func_1(parab_a, parab_b, parab_c)(curr_input), 0))

            dot_label = MathTex(r"(", round(curr_input, 2), r",",  round(func_1(parab_a, parab_b, parab_c)(curr_input), 2), r")").next_to(geometric_dot, DOWN, buff = .1).shift(RIGHT)

            dot_label[1].set_color(BLUE)
            dot_label[3].set_color(BLUE)

            return VGroup(geometric_dot, dot_label)
        
        moving_turning_point = always_redraw(lambda : turning_point_dot(parabola_a.get_value(),
                                                                        parabola_b.get_value(),
                                                                        parabola_c.get_value()))

        self.play(Write(moving_turning_point))
        self.wait()
        self.play(Write(math_implications[1]), run_time = 2)
        self.wait()
        
        for k in range(2, len(math_implications)):

            self.play(Write(math_implications[k]), run_time = 2)
            self.wait()
        
        self.wait(5)

        pass

    pass

class Cubic(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{3.\ \text{Polynomial function}}").scale(1.2).next_to(header_position, RIGHT)

        math_def = MathTex(r"f(x) &= a_3x^3 + a_2x^2 + a_1x + a_0\\ ",
                           tex_template = myTemplate)
        
        color_text(r_list = [],
                   g_list = [],
                   y_list = [(0, 2, 1), (0, 7, 1), (0, 12, 1), (0, 17, 1), ],
                   b_list = [(0, 5, 2), (0, 10, 2), (0, 15, 2), (0, 19, 2), ],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{$a_nx^n + \cdots + a_1x + a_0$}\\ ",
                                r"2.\quad & \text{Sum and product formulae}\\ ",
                                r"3.\quad & \text{Remainder and factor theorems}\\ ",
                                r"4.\quad & \text{Fundamental theorem of algebra}\\ ",
                                r"5.\quad & \text{Ring theory}\\ ",
                                tex_template = myTemplate).scale(.9)
        
        color_text(r_list = [],
                   g_list = [],
                   y_list = [(0, 4, 1), (0, 13, 1), ],
                   b_list = [(0, 2, 2), (0, 11, 2), (0, 15, 2), ],
                   formula = math_implications)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-2.3, 2.3],
            y_range=[-14, 6],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"x").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        parabola_a = ValueTracker(1)
        parabola_b = ValueTracker(0)
        parabola_c = ValueTracker(0)

        def func_1():

            return lambda x : (x ** 3) - (x ** 2) - (5*x / 4) + 3/4

        graph_pic = always_redraw(lambda : ax.plot(func_1(), x_range=[-2.2, 2.2, 0.01], color=YELLOW).set_z_index(-1))

        def graph_relabel():

            curr_tex = MathTex(r"y = f(x)").next_to(ax.c2p(2.2, func_1()(2.2), 0), UP)
            curr_tex[0][0].set_color(YELLOW)
            curr_tex[0][4].set_color(YELLOW)

            return curr_tex

        graph_label = always_redraw(lambda : graph_relabel())

        color_text(y_list = [],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_label, graph_pic
               ).move_to(diagram_position.get_center())
        
        self.play(Write(header))
        self.wait()
        
        self.play(Write(math_def[0]))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()

        def intercept_dot(curr_int):

            geometric_dot = Dot().move_to(ax.c2p(0, curr_int, 0))

            dot_label = MathTex(r"(0,", round(curr_int, 2), r")").next_to(geometric_dot, DL, buff = .1)

            return VGroup(geometric_dot, dot_label)
        
        ### math-implications

        for k in range(len(math_implications)):

            self.play(Write(math_implications[k]), run_time = 2)
            self.wait()
        
        self.wait(5)

        pass

    pass

class Rational(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{4.\ \text{Reciprocal functions}}").scale(1.2).next_to(header_position, RIGHT)

        math_def = MathTex(r"f(x) &= \frac{1}{x}\\ ",
                           tex_template = myTemplate)
        
        color_text(r_list = [],
                   g_list = [],
                   y_list = [(0, 2, 1), (0, 7, 1), ],
                   b_list = [],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{Asymptotes}\\ ",
                                r"2.\quad & \text{Inverse proportion}\\ ",
                                r"3.\quad & \text{Ideal gas law}\\ ",
                                r"4.\quad & \text{$\deriv{}{x} \ln(x) = 1/x$}\\ ",
                                r"5.\quad & \text{Inverse-square law}\\ ",
                                r"6.\quad & \text{Newton's law of gravitation}\\ ",
                                tex_template = myTemplate).scale(.9)
        
        math_implications[3][5].set_color(YELLOW)
        math_implications[3][9].set_color(YELLOW)
        math_implications[3][14].set_color(YELLOW)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-5.3, 5.3],
            y_range=[-5.3, 5.3],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"x").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        def func_1(n):

            return lambda x : 1/(x ** n)
        
        graph_label = MathTex(r"y = f(x)").next_to(ax.c2p(5, func_1(1)(5), 0), UP)
        graph_label[0][0].set_color(YELLOW)
        graph_label[0][-2].set_color(YELLOW)

        color_text(y_list = [],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_label, 
               ).move_to(diagram_position.get_center())
        
        def reciprocal(n):

            right_branch = ax.plot(func_1(n), x_range=[5, (.2) ** (1 / n), -0.01], color=YELLOW).set_z_index(-1)
            left_branch = ax.plot(func_1(n), x_range=[-5, -(.2) ** (1 / n), 0.01], color=YELLOW).set_z_index(-1)

            return VGroup(right_branch, left_branch)

        graph_pic = reciprocal(1)
        
        self.play(Write(header))
        self.wait()
        
        self.play(Write(math_def[0]))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()

        ### math-implications

        for k in range(4):

            if k == 0:
                self.play(Indicate(ax))
                self.wait()

            self.play(Write(math_implications[k]), run_time = 2)
            self.wait()
        
        def reciprocal_tex(n):

            if n == 2:
                curr_tex = MathTex(r"f(x) &= \frac{1}{x^2} ", tex_template = myTemplate)
            elif n == 3:
                curr_tex = MathTex(r"f(x) &= \frac{1}{x^3} ", tex_template = myTemplate)
            elif n == 4:
                curr_tex = MathTex(r"f(x) &= \frac{1}{x^4} ", tex_template = myTemplate)
            elif n == 5:
                curr_tex = MathTex(r"f(x) &= \frac{1}{x^5} ", tex_template = myTemplate)

            curr_tex[0][2].set_color(YELLOW)
            curr_tex[0][7].set_color(YELLOW)
            curr_tex[0][8].set_color(BLUE)

            return curr_tex

        self.play(Transform(math_def, reciprocal_tex(2).move_to(math_def)),
                  Transform(graph_pic, reciprocal(2)), run_time = 1.5)
        self.wait()
        
        self.play(Write(math_implications[4]), run_time = 2)
        self.wait()
        self.play(Write(math_implications[5]), run_time = 2)
        self.wait()

        self.play(Transform(math_def, reciprocal_tex(3).move_to(math_def)),
                  Transform(graph_pic, reciprocal(3)), run_time = 2)
        self.play(Transform(math_def, reciprocal_tex(4).move_to(math_def)),
                  Transform(graph_pic, reciprocal(4)), run_time = 2)
        self.play(Transform(math_def, reciprocal_tex(5).move_to(math_def)),
                  Transform(graph_pic, reciprocal(5)), run_time = 2)

        self.wait(5)

        pass

    pass

class SquareRoot(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{5.\ \text{Square root function}}").scale(1.2).next_to(header_position, RIGHT)
        header_2 = MathTex(r"\underline{6.\ \text{$n$-th root function}}").scale(1.2).next_to(header_position, RIGHT)
        header_2[0][2].set_color(BLUE)

        math_def = MathTex(r"f(x) &= \sqrt{x}\\ ",
                           tex_template = myTemplate)
        
        color_text(r_list = [],
                   g_list = [],
                   y_list = [(0, 2, 1), (0, -1, 1), ],
                   b_list = [],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$}\\ ",
                                r"2.\quad & \text{$x^5 - x - 1 = 0$}\\ ",
                                tex_template = myTemplate).scale(.9)
        
        color_text(r_list = [(0, 13, 1), (0, 17, 1), ],
                   g_list = [(0, 14, 1), ],
                   y_list = [(0, 2, 1), (1, 2, 2), (1, 5, 1), ],
                   b_list = [(0, 5, 1), (0, 9, 1), ],
                   formula = math_implications)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-1.1, 1.1],
            y_range=[-1.1, 1.1],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"x").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        def func_1(n):

            return lambda x : x ** (1/n)
        
        graph_label = MathTex(r"y = f(x)").next_to(ax.c2p(1, 1, 0), UP)
        graph_label[0][0].set_color(YELLOW)
        graph_label[0][-2].set_color(YELLOW)

        color_text(y_list = [],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_label, 
               ).move_to(diagram_position.get_center())
        
        def root_function(n):

            right_branch = ax.plot(func_1(n), x_range=[0, 1, 0.01], color=YELLOW).set_z_index(-1)

            if n % 2:

                left_branch = right_branch.copy()
                left_branch.rotate(PI, about_point=ax.c2p(0,0,0))

                return VGroup(right_branch, left_branch)
            
            else:

                return right_branch

        graph_pic = root_function(2)
        
        self.play(Write(header))
        self.wait()
        
        self.play(Write(math_def[0]))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()

        ### math-implications

        self.play(Write(math_implications[0]), run_time = 2)
        self.wait()

        def nth_root_tex(n):

            if n == 3:

                curr_tex = MathTex(r"f(x) &= \sqrt[3]{x} ", tex_template = myTemplate)

            elif n == 4:

                curr_tex = MathTex(r"f(x) &= \sqrt[4]{x} ", tex_template = myTemplate)

            elif n == 5:

                curr_tex = MathTex(r"f(x) &= \sqrt[5]{x} ", tex_template = myTemplate)

            curr_tex[0][2].set_color(YELLOW)
            curr_tex[0][5].set_color(BLUE)
            curr_tex[0][8].set_color(YELLOW)

            return curr_tex
        
        self.play(Transform(math_def, nth_root_tex(3).move_to(math_def)),
                  Transform(graph_pic, root_function(3)), run_time = 1.5)
        self.wait()

        self.play(Transform(math_def, nth_root_tex(4).move_to(math_def)),
                  Transform(graph_pic, root_function(4)), run_time = 2)
        self.play(Transform(math_def, nth_root_tex(5).move_to(math_def)),
                  Transform(graph_pic, root_function(5)), run_time = 2)
        
        self.wait()

        self.play(Transform(header, header_2), run_time = 2)
        self.wait()
        self.play(Write(math_implications[1]), run_time = 2)
        self.wait()

        self.wait(5)

        pass

    pass

### TRIGONOMETRIC

class Sine(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{7.\ \text{Sine graph}}").scale(1.2).next_to(header_position, RIGHT)

        math_def = MathTex(r"f(t) &= A\sin(\omega t + \varphi)\\ ",
                           r"\omega  &= ", r"-1.00\\ ",
                           r"\varphi &= ", r"-1.00\\ ",
                           r"A &= ", r"-1.00\\ ",
                           tex_template = myTemplate)
        
        color_text(r_list = [(0, 5, 1), (5, 0, 1), ],
                   g_list = [(0, 13, 1), (3, 0, 1), ],
                   y_list = [(0, 2, 1), (0, 11, 1), ],
                   b_list = [(0, 10, 1), (1, 0, 1), ],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{Period $2\pi/\omega$}\\ ",
                                r"2.\quad & \text{Simple harmonic motion}\\ ",
                                r"3.\quad & \text{Light and sound waves}\\ ",
                                r"4.\quad & \text{Trigonometric identities}",
                                tex_template = myTemplate).scale(.9)
        
        math_implications[0][-1].set_color(BLUE)
        math_implications[0][-4:-2].set_color(GOLD)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-.5, 7],
            y_range=[-2.5, 2.5],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"t").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        sin_omega = ValueTracker(1)
        sin_phi = ValueTracker(0)
        sin_amp = ValueTracker(1)

        parabola_a_tex = always_redraw(lambda : MathTex(round(sin_omega.get_value(), 2)).move_to(math_def[2]).set_color(BLUE))
        parabola_b_tex = always_redraw(lambda : MathTex(round(sin_phi.get_value(), 2)).move_to(math_def[4]).set_color(GREEN))
        parabola_c_tex = always_redraw(lambda : MathTex(round(sin_amp.get_value(), 2)).move_to(math_def[6]).set_color(RED))

        def func_1(omega, phi, amp):

            return lambda x : amp * np.sin(omega * x + phi)
        
        def func_2(omega, phi, amp):

            return lambda x : amp * np.cos(omega * x + phi)

        graph_pic = always_redraw(lambda : ax.plot(func_1(sin_omega.get_value(), sin_phi.get_value(), sin_amp.get_value()), x_range=[0, TAU, 0.01], color=YELLOW).set_z_index(-1))

        def graph_label_tex(omeg, phii, ampp, input_val):

            curr_tex = MathTex(r"y = f(t)").next_to(ax.c2p(TAU, func_1(omeg, phii, ampp)(input_val), 0), UP)
            curr_tex[0][0].set_color(YELLOW)
            curr_tex[0][4].set_color(YELLOW)

            return curr_tex

        graph_label = always_redraw(lambda : graph_label_tex(sin_omega.get_value(), sin_phi.get_value(), sin_amp.get_value(), TAU))

        color_text(y_list = [],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_pic, graph_label
               ).move_to(diagram_position.get_center())
        
        main_func_def = math_def[0]

        self.play(Write(header))
        self.wait()
        
        self.play(Write(main_func_def))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()

        self.play(Write(math_def[1]))
        self.play(Write(parabola_a_tex))
        self.wait()

        self.play(sin_omega.animate.set_value(3), run_time = 3)
        self.wait()
        self.play(sin_omega.animate.set_value(.5), run_time = 3)
        self.wait()
        self.play(sin_omega.animate.set_value(2), run_time = 3)
        self.wait()

        self.play(Write(math_def[3]))
        self.play(Write(parabola_b_tex))
        self.wait()

        self.play(sin_phi.animate.set_value(-TAU), run_time = 3)
        self.wait()
        self.play(sin_phi.animate.set_value(TAU), run_time = 3)
        self.wait()
        self.play(sin_phi.animate.set_value(0), run_time = 3)
        self.wait()

        self.play(Write(math_def[5]))
        self.play(Write(parabola_c_tex))
        self.wait()

        self.play(sin_amp.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(sin_amp.animate.set_value(1/2), run_time = 3)
        self.wait()
        self.play(sin_amp.animate.set_value(2), run_time = 3)
        self.wait()

        ### math-implications

        period_brace = BraceLabel(Line(ax.c2p(0,0,0), ax.c2p(PI,0,0)), r"\text{Period}")

        self.play(Write(period_brace), run_time = 1.5)
        self.wait()
        self.play(period_brace.animate.next_to(period_brace, RIGHT, buff = 0), run_time = 1.5)
        self.wait()

        self.play(Write(math_implications[0]), run_time = 2)
        self.wait()

        self.play(Write(math_implications[1]), run_time = 2)
        self.wait()

        self.play(Write(math_implications[2]), run_time = 2)
        self.wait()

        ### change to cosine

        graph_pic_static = ax.plot(func_1(sin_omega.get_value(), sin_phi.get_value(), sin_amp.get_value()), x_range=[0, TAU, 0.01], color=YELLOW).set_z_index(-1)
        
        self.remove(graph_pic)
        self.add(graph_pic_static)
        
        header_2 = MathTex(r"\underline{8.\ \text{Cosine graph}}").scale(1.2).next_to(header_position, RIGHT)

        math_def_2 = MathTex(r"f(t) &= A\cos(\omega t + \varphi)\\ ",
                           tex_template = myTemplate).move_to(math_def[0])
        
        color_text(r_list = [(0, 5, 1), ],
                   g_list = [(0, 13, 1), ],
                   y_list = [(0, 2, 1), (0, 11, 1), ],
                   b_list = [(0, 10, 1), ],
                   formula = math_def_2)

        graph_pic_2 = ax.plot(func_2(sin_omega.get_value(), sin_phi.get_value(), sin_amp.get_value()), x_range=[0, TAU, 0.01], color=YELLOW).set_z_index(-1)

        graph_label_static =  MathTex(r"y = f(t)").next_to(ax.c2p(TAU, func_1(sin_omega.get_value(), sin_phi.get_value(), sin_amp.get_value())(TAU), 0), UP)
        graph_label_static[0][0].set_color(YELLOW)
        graph_label_static[0][4].set_color(YELLOW)
        
        self.remove(graph_label)
        self.add(graph_label_static)

        graph_label_2 = MathTex(r"y = f(t)").next_to(ax.c2p(TAU, func_2(sin_omega.get_value(), sin_phi.get_value(), sin_amp.get_value())(TAU), 0), UP)
        graph_label_2[0][0].set_color(YELLOW)
        graph_label_2[0][4].set_color(YELLOW)

        self.play(Transform(main_func_def, math_def_2), 
                  Transform(header, header_2), run_time = 2)
        
        self.wait()

        self.play(Transform(graph_pic_static, graph_pic_2), 
                  Transform(graph_label_static, graph_label_2), run_time = 2)
        
        self.wait()

        self.play(period_brace.animate.next_to(period_brace, LEFT, buff = 0), run_time = 1.5)
        self.wait()
        self.play(Write(math_implications[3]), run_time = 2)
        self.wait()
        
        self.wait(5)

        pass

    pass

class Tangent(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{9.\ \text{Tangent graph}}").scale(1.2).next_to(header_position, RIGHT)


        math_def = MathTex(r"f(\theta) &= \tan(\theta)\\ ",
                           tex_template = myTemplate)
        
        for i in [2, 9]:

            math_def[0][i].set_color(YELLOW)
        
        color_text(r_list = [],
                   g_list = [],
                   y_list = [],
                   b_list = [],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{Asymptotes}\\ ",
                                r"2.\quad & \text{Gradients}\\ ",
                                r"3.\quad & \text{Calculus}\\ ",
                                r"4.\quad & \text{Complex numbers}\\ ",
                                tex_template = myTemplate).scale(.9)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-3.5, 3.5],
            y_range=[-3, 3],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"\theta").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        def func_1():

            return lambda x : np.tan(x)

        def func_2():

            return lambda x : 1 / np.tan(x)
        
        def func_3():

            return lambda x : 1 / np.cos(x)
        
        def func_4():

            return lambda x : 1 / np.sin(x)

        graph_pic = ax.plot(func_1(), x_range=[-PI, PI, 0.01], discontinuities=[-PI/2, PI/2], dt=0.35, color=YELLOW).set_z_index(-1)
        
        graph_label = MathTex(r"y = f(\theta)").next_to(ax.c2p(PI, func_1()(PI), 0), UP)

        for i in [0, 4]:

            graph_label[0][i].set_color(YELLOW)

        color_text(y_list = [],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_label, graph_pic
               ).move_to(diagram_position.get_center())
        
        self.play(Write(header))
        self.wait()
        
        self.play(Write(math_def[0]))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()

        def intercept_dot(curr_int):

            geometric_dot = Dot().move_to(ax.c2p(0, curr_int, 0))

            dot_label = MathTex(r"(0,", round(curr_int, 2), r")").next_to(geometric_dot, DL, buff = .1)

            return VGroup(geometric_dot, dot_label)
        
        ### math-implications

        asymptotes = VGroup(DashedLine(ax.c2p(-PI/2, -2.9, 0), ax.c2p(-PI/2, 2.9, 0)),
                            DashedLine(ax.c2p(PI/2, -2.9, 0), ax.c2p(PI/2, 2.9, 0)))
        
        self.play(Write(asymptotes), run_time = 2)
        self.wait()

        self.play(Write(math_implications[0]), run_time = 2)
        self.wait()

        for k in range(1, len(math_implications)):

            self.play(Write(math_implications[k]), run_time = 2)
            self.wait()
        
        ### conversion to periodic functions

        period_brace = BraceLabel(Line(ax.c2p(-PI,0,0), ax.c2p(0,0,0)), r"T").set_color(GOLD)
        self.play(Write(period_brace))
        self.wait()
        self.play(period_brace.animate.next_to(period_brace, RIGHT, buff = 0))
        self.wait()
        
        math_def_2 = MathTex(r"f(\theta) &= f(\theta + T)\\ ",
                           tex_template = myTemplate).move_to(math_def)
        
        math_def_2[0][2].set_color(YELLOW)
        math_def_2[0][7].set_color(YELLOW)
        math_def_2[0][9].set_color(GOLD)
        
        self.play(Transform(header, MathTex(r"\underline{10.\ \text{Periodic graph}}").scale(1.2).next_to(header_position, RIGHT)),
                  Transform(math_def, math_def_2))
        
        self.wait(2)
        
        ### conversion to cotangent function
        
        math_def_2 = MathTex(r"f(\theta) &= \dsfrac{1}{\tan(\theta)} \equiv \cot(\theta)\\ ",
                           tex_template = myTemplate).move_to(math_def)
        
        for i in [2, 11, 18]:
            math_def_2[0][i].set_color(YELLOW)
        
        self.play(Transform(header, MathTex(r"\underline{11.\ \text{Cotangent graph}}").scale(1.2).next_to(header_position, RIGHT)),
                  Transform(math_def, math_def_2),
                  FadeOut(period_brace))
        self.wait()

        graph_pic_new = ax.plot(func_2(), x_range=[-PI+.35, PI-.35, 0.01], discontinuities=[0,], dt=0.35, color=YELLOW).set_z_index(-1)

        func_tex = MathTex(r"y = f(\theta)")
        func_tex[0][0].set_color(YELLOW)
        func_tex[0][-2].set_color(YELLOW)

        self.play(Transform(graph_pic, graph_pic_new),
                  Transform(asymptotes, VGroup(DashedLine(ax.c2p(-PI, -2.9, 0), ax.c2p(-PI, 2.9, 0)),
                                               DashedLine(ax.c2p(PI, -2.9, 0), ax.c2p(PI, 2.9, 0)))),
                                               Transform(graph_label, func_tex.next_to(ax.c2p(PI-.35, func_2()(PI-.35), 0), DOWN))
                                               )
        self.wait(2)
        
        ### conversion to cosecant function
        
        math_def_2 = MathTex(r"f(\theta) &= \dsfrac{1}{\sin(\theta)} \equiv \csc(\theta)\\ ",
                           tex_template = myTemplate).move_to(math_def)
        
        for i in [2, 11, 18]:
            math_def_2[0][i].set_color(YELLOW)

        self.play(Transform(header, MathTex(r"\underline{12.\ \text{Cosecant graph}}").scale(1.2).next_to(header_position, RIGHT)),
                  Transform(math_def, math_def_2))
        self.wait()

        graph_pic_new = ax.plot(func_4(), x_range=[-PI+.35, PI-.35, 0.01], discontinuities=[0,], dt=0.35, color=YELLOW).set_z_index(-1)

        self.play(Transform(graph_pic, graph_pic_new),
                  Transform(graph_label, func_tex.next_to(ax.c2p(PI-.35, func_4()(PI-.35), 0), UP)))
        self.wait(2)
        
        ### conversion to cosecant function
        
        math_def_3 = MathTex(r"f(\theta) &= \dsfrac{1}{\cos(\theta)} \equiv \sec(\theta)\\ ",
                           tex_template = myTemplate).move_to(math_def)
        
        for i in [2, 11, 18]:
            math_def_3[0][i].set_color(YELLOW)

        self.play(Transform(header, MathTex(r"\underline{13.\ \text{Secant graph}}").scale(1.2).next_to(header_position, RIGHT)),
                  Transform(math_def, math_def_3))
        self.wait()

        graph_pic_new = ax.plot(func_3(), x_range=[-PI, PI, 0.01], discontinuities=[-PI/2, PI/2], dt=0.35, color=YELLOW).set_z_index(-1)

        self.play(Transform(graph_pic, graph_pic_new),
                  Transform(asymptotes, VGroup(DashedLine(ax.c2p(-PI/2, -2.9, 0), ax.c2p(-PI/2, 2.9, 0)),
                                               DashedLine(ax.c2p(PI/2, -2.9, 0), ax.c2p(PI/2, 2.9, 0)))),
                  Transform(graph_label, func_tex.next_to(ax.c2p(PI, func_3()(PI), 0), RIGHT)))
        self.wait(2)
        
        self.wait(5)

        pass

    pass

### ANALYTIC

class Exponential(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{14.\ \text{Exponential graph $\nearrow$}}").scale(1.2).next_to(header_position, RIGHT)
        
        header_2 = MathTex(r"\underline{15.\ \text{Exponential graph $\searrow$}}").scale(1.2).next_to(header_position, RIGHT)

        math_def = MathTex(r"f(t) &= ", r"f(0) e^{-kt}\\ ",
                           r"f(0) &= ", r"-0.50\\ ",
                           r"k &= ", r"-1.00\\ ",
                           tex_template = myTemplate)
        
        color_text(r_list = [(1, 6, 1), (4, 0, 1), ],
                   g_list = [(1, 2, 1), (2, 2, 1), ],
                   y_list = [(0, 2, 1), (1, 7, 1), ],
                   b_list = [],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{Initial amount: $f(0)$}\\ ",
                                r"2.\quad & \text{Growth rate: $k$}\\ ",
                                r"3.\quad & \text{Compound interest}\\ ",
                                r"4.\quad & \text{$f'(t) = f(t)$}\\ ",
                                r"5.\quad & \text{Population growth}\\ ",
                                r"6.\quad & \text{Radioactive decay}",
                                tex_template = myTemplate).scale(.7)
        
        color_text(r_list = [(1, -1, 1), ],
                   g_list = [(0, -2, 1), ],
                   y_list = [(3, -7, 1), (3, -2, 1), ],
                   b_list = [],
                   formula = math_implications)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-5.5, 5.5],
            y_range=[-2, 10],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"t").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        expo_initial = ValueTracker(1)
        expo_quick = ValueTracker(1)

        init_tex = always_redraw(lambda : MathTex(round(expo_initial.get_value(), 2)).move_to(math_def[3]).set_color(GREEN))
        quick_tex = always_redraw(lambda : MathTex(round(expo_quick.get_value(), 2)).move_to(math_def[5]).set_color(RED))

        def func_1(init, quickness):

            return lambda x : init * np.exp(quickness * x)
        
        def func_2(init, quickness):

            return lambda x : init * np.exp(-quickness * x)
        
        def upper_limit_value(init, quickness, M):

            return np.log(M / init) / quickness
        
        graph_pic = always_redraw(lambda : ax.plot(func_1(expo_initial.get_value(), expo_quick.get_value()), x_range=[-5, upper_limit_value(expo_initial.get_value(), expo_quick.get_value(), 9), 0.01], color=YELLOW).set_z_index(-1))

        def graph_label_tex(initial, quick):

            curr_tex = MathTex(r"y = f(t)").next_to(ax.c2p(upper_limit_value(initial, quick, 9),
                                                                                 func_1(initial, quick)(upper_limit_value(initial, quick, 9)), 0), UP)
            
            curr_tex[0][0].set_color(YELLOW)
            curr_tex[0][4].set_color(YELLOW)

            return curr_tex
        
        graph_label = always_redraw(lambda : graph_label_tex(expo_initial.get_value(), expo_quick.get_value()))

        color_text(y_list = [],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_pic, graph_label
               ).move_to(diagram_position.get_center())
        
        self.play(Write(header))
        self.wait()
        
        math_def_pos = MathTex(r"f(0) e^{kt}").move_to(math_def[1])
        math_def_pos[0][2].set_color(GREEN)
        math_def_pos[0][5].set_color(RED)
        math_def_pos[0][6].set_color(YELLOW)
        
        self.play(Write(math_def[0]))
        self.play(Write(math_def_pos))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()

        self.play(Write(math_def[2]))
        self.play(Write(init_tex))
        self.wait()

        self.play(Write(math_def[4]))
        self.play(Write(quick_tex))
        self.wait()

        def intercept_dot(curr_int):

            geometric_dot = Dot().move_to(ax.c2p(0, curr_int, 0))

            dot_label = MathTex(r"(0,", round(curr_int, 2), r")").next_to(geometric_dot, UL, buff = .1)
            dot_label[0][1].set_color(GREEN)
            dot_label[1].set_color(GREEN)

            return VGroup(geometric_dot, dot_label)
        
        moving_intercept = always_redraw(lambda : intercept_dot(expo_initial.get_value()))

        self.play(Write(moving_intercept))
        self.wait()

        self.play(expo_initial.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(expo_initial.animate.set_value(0.1), run_time = 3)
        self.wait()

        self.play(Write(math_implications[0]), run_time = 2)
        self.wait()
        self.play(expo_initial.animate.set_value(1), run_time = 3)
        self.wait()

        self.play(expo_quick.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(expo_quick.animate.set_value(0.4), run_time = 3)
        self.wait()

        self.play(Write(math_implications[1]), run_time = 2)
        self.wait()
        self.play(expo_quick.animate.set_value(0.5), run_time = 3)
        self.wait()
        
        self.play(Write(math_implications[2]), run_time = 2)
        self.wait()
        self.play(Write(math_implications[3]), run_time = 2)
        self.wait()
        self.play(Write(math_implications[4]), run_time = 2)
        self.wait()

        ### switch to negative k

        self.play(Transform(math_def_pos, math_def[1]))
        self.wait()
        
        graph_pic_static = ax.plot(func_1(expo_initial.get_value(), expo_quick.get_value()), x_range=[-5, upper_limit_value(expo_initial.get_value(), expo_quick.get_value(), 9), 0.01], color=YELLOW).set_z_index(-1)

        graph_pic_2 = always_redraw(lambda : ax.plot(func_2(expo_initial.get_value(), expo_quick.get_value()), x_range=[-upper_limit_value(expo_initial.get_value(), expo_quick.get_value(), 9), 5, 0.01], color=YELLOW).set_z_index(-1))

        graph_pic_2_static = ax.plot(func_2(expo_initial.get_value(), expo_quick.get_value()), x_range=[-upper_limit_value(expo_initial.get_value(), expo_quick.get_value(), 9), 5, 0.01], color=YELLOW).set_z_index(-1)
        
        graph_label_static = MathTex(r"y = f(t)").next_to(ax.c2p(upper_limit_value(expo_initial.get_value(), expo_quick.get_value(), 9), func_1(expo_initial.get_value(), expo_quick.get_value())(upper_limit_value(expo_initial.get_value(), expo_quick.get_value(), 9)), 0), UP)
        graph_label_static[0][0].set_color(YELLOW)
        graph_label_static[0][4].set_color(YELLOW)

        
        def graph_label_2_tex(initial, quick):

            curr_tex = MathTex(r"y = f(t)").next_to(ax.c2p(-upper_limit_value(initial, quick, 9), func_2(initial, quick)(-upper_limit_value(initial, quick, 9)), 0), UP)
            
            curr_tex[0][0].set_color(YELLOW)
            curr_tex[0][4].set_color(YELLOW)

            return curr_tex

        graph_label_2 = always_redraw(lambda : graph_label_2_tex(expo_initial.get_value(), expo_quick.get_value()))

        graph_label_2_static = MathTex(r"y = f(t)").next_to(ax.c2p(-upper_limit_value(expo_initial.get_value(), expo_quick.get_value(), 9), func_2(expo_initial.get_value(), expo_quick.get_value())(-upper_limit_value(expo_initial.get_value(), expo_quick.get_value(), 9)), 0), UP)
        graph_label_2_static[0][0].set_color(YELLOW)
        graph_label_2_static[0][4].set_color(YELLOW)

        moving_intercept_static = intercept_dot(expo_initial.get_value())
        
        def intercept_dot_right(curr_int):

            geometric_dot = Dot().move_to(ax.c2p(0, curr_int, 0))

            dot_label = MathTex(r"(0,", round(curr_int, 2), r")").next_to(geometric_dot, UR, buff = .1)
            dot_label[0][1].set_color(GREEN)
            dot_label[1].set_color(GREEN)

            return VGroup(geometric_dot, dot_label)
        
        moving_intercept_right_static = intercept_dot_right(expo_initial.get_value())

        moving_intercept_right = always_redraw(lambda : intercept_dot_right(expo_initial.get_value()))

        self.add(graph_pic_static, graph_label_static, moving_intercept_static)
        self.remove(graph_pic, graph_label, moving_intercept)

        self.play(Transform(graph_pic_static, graph_pic_2_static),
                  Transform(graph_label_static, graph_label_2_static),
                  Transform(moving_intercept_static, moving_intercept_right_static),
                  Transform(header, header_2),
                  run_time = 2)
        self.wait()
        self.add(graph_pic_2, graph_label_2, moving_intercept_right)
        self.remove(graph_pic_static, graph_label_static, moving_intercept_static)

        self.play(expo_quick.animate.set_value(1), run_time = 3)
        self.wait()

        self.play(expo_initial.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(expo_initial.animate.set_value(0.1), run_time = 3)
        self.wait()
        self.play(expo_initial.animate.set_value(1), run_time = 3)
        self.wait()

        self.play(expo_quick.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(expo_quick.animate.set_value(0.4), run_time = 3)
        self.wait()
        self.play(expo_quick.animate.set_value(0.5), run_time = 3)
        self.wait()

        ### TBC: circumscribe growth rate, change to decay rate

        implication_edit = VGroup(SurroundingRectangle(math_implications[1], buff = .1).set_color(RED))
        implication_edit.add(Tex(r"Decay rate").set_color(RED).scale(.7).next_to(implication_edit[0], RIGHT))

        self.play(Write(implication_edit[0]))
        self.play(Write(implication_edit[1]))
        self.wait()

        self.play(Write(math_implications[5]), run_time = 2)
        self.wait()
        
        self.wait(5)

        pass

    pass

class ExponentialGen(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{16.\ \text{General exponential graph}}").scale(1.2).next_to(header_position, RIGHT)
        
        math_def = MathTex(r"f(t) &= f(0) a^t\\ ",
                           r"f(0) &= ", r"-0.50\\ ",
                           r"a &= ", r"-1.00\\ ",
                           tex_template = myTemplate)
        
        color_text(r_list = [(0, 9, 1), (3, 0, 1), ],
                   g_list = [(0, 7, 1), (1, 2, 1), ],
                   y_list = [(0, 2, 1), (0, 10, 1), ],
                   b_list = [],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{Initial amount: $f(0)$}\\ ",
                                r"2.\quad & \text{Multiplier: $a$}\\ ",
                                r"3.\quad & \text{Compound interest}\\ ",
                                tex_template = myTemplate)
        
        math_implications[0][-2].set_color(GREEN)
        math_implications[1][-1].set_color(RED)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-5.5, 5.5],
            y_range=[-2, 10],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"t").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        expo_initial = ValueTracker(1)
        expo_quick = ValueTracker(2)

        init_tex = always_redraw(lambda : MathTex(round(expo_initial.get_value(), 2)).move_to(math_def[2]).set_color(GREEN))
        quick_tex = always_redraw(lambda : MathTex(round(expo_quick.get_value(), 2)).move_to(math_def[4]).set_color(RED))

        def func_1(init, quickness):

            return lambda x : init * np.exp(np.log(quickness) * x)
        
        def upper_limit_value(init, quickness, M):

            return np.log(M / init) / np.log(quickness)
        
        def lower_limit_value(init, quickness, m):

            return np.log(m / init) / np.log(quickness)
        
        def required_domain(init, quickness, m, M):

            if quickness > 1:

                larger = min(5, upper_limit_value(init, quickness, M))
                smaller = max(-5, lower_limit_value(init, quickness, m))

                return [smaller, larger, 0.01]
            
            elif quickness < 1:

                larger = min(5, lower_limit_value(init, quickness, m))
                smaller = max(-5, upper_limit_value(init, quickness, M))
                
                return [smaller, larger, 0.01]
            
            else:

                return [-5, 5, 0.01]
        
        graph_pic = always_redraw(lambda : ax.plot(func_1(expo_initial.get_value(), expo_quick.get_value()),
                                                   x_range = required_domain(expo_initial.get_value(), expo_quick.get_value(), 0.01, 9),
                                                   color=YELLOW).set_z_index(-1))

        def graph_label_tex(initial, quickness):

            curr_tex = MathTex(r"y = f(t)").next_to(ax.c2p(upper_limit_value(initial, quickness, 9), func_1(initial, quickness)(upper_limit_value(initial, quickness, 9)), 0), UP)
            curr_tex[0][0].set_color(YELLOW)
            curr_tex[0][4].set_color(YELLOW)

            return curr_tex
        
        graph_label = always_redraw(lambda : graph_label_tex(expo_initial.get_value(), expo_quick.get_value()))

        color_text(y_list = [],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_pic, graph_label
               ).move_to(diagram_position.get_center())
        
        self.play(Write(header))
        self.wait()
        
        self.play(Write(math_def[0]))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()

        self.play(Write(math_def[1]))
        self.play(Write(init_tex))
        self.wait()

        self.play(Write(math_def[3]))
        self.play(Write(quick_tex))
        self.wait()

        def intercept_dot(curr_int):

            geometric_dot = Dot().move_to(ax.c2p(0, curr_int, 0))

            dot_label = MathTex(r"(0,", round(curr_int, 2), r")").next_to(geometric_dot, UL, buff = .1)
            dot_label[0][1].set_color(GREEN)
            dot_label[1].set_color(GREEN)

            return VGroup(geometric_dot, dot_label)
        
        moving_intercept = always_redraw(lambda : intercept_dot(expo_initial.get_value()))

        self.play(Write(moving_intercept))
        self.wait()

        self.play(expo_initial.animate.set_value(2), run_time = 3)
        self.wait()
        self.play(expo_initial.animate.set_value(0.1), run_time = 3)
        self.wait()

        self.play(Write(math_implications[0]), run_time = 2)
        self.wait()
        self.play(expo_initial.animate.set_value(1), run_time = 3)
        self.wait()

        self.play(expo_quick.animate.set_value(4), run_time = 3)
        self.wait()
        self.play(expo_quick.animate.set_value(1), run_time = 3)
        self.wait(2)
        self.play(expo_quick.animate.set_value(0.25), run_time = 3)
        self.wait(2)
        self.play(expo_quick.animate.set_value(2), run_time = 6)
        self.wait()

        self.play(Write(math_implications[1]), run_time = 2)
        self.wait()
        
        self.play(Write(math_implications[2]), run_time = 2)
        self.wait()
        self.wait(5)

    pass

class Logarithm(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{17.\ \text{Natural logarithm graph}}").scale(1.2).next_to(header_position, RIGHT)
        
        header_2 = MathTex(r"\underline{18.\ \text{General logarithm graph}}").scale(1.2).next_to(header_position, RIGHT)
        
        math_def = MathTex(r"f(x) &= ", r"\log_a(x - c)\\ ",
                           r"c &= ", r"-1.00\\ ",
                           r"a &= ", r"-1.00\\ ",
                           tex_template = myTemplate)
        
        color_text(r_list = [(1, 3, 1), (4, 0, 1), ],
                   g_list = [],
                   y_list = [(0, 2, 1), (1, 5, 1), ],
                   b_list = [(1, 7, 1), (2, 0, 1), ],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{Asymptote $x = c$}\\ ",
                                r"2.\quad & \text{``Stretcher'': $a$}\\ ",
                                r"3.\quad & \text{Exponential equations}\\ ",
                                tex_template = myTemplate)
        
        color_text(r_list = [(1, -1, 1), ],
                   g_list = [],
                   y_list = [(0, -3, 1), ],
                   b_list = [(0, -1, 1), ],
                   formula = math_implications)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-2, 10],
            y_range=[-5.5, 5.5],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=7*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"x").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        asymptote_anim = ValueTracker(0)
        log_base_anim = ValueTracker(np.exp(1))

        asymptote_tex = always_redraw(lambda : MathTex(round(asymptote_anim.get_value(), 2)).move_to(math_def[3]).set_color(BLUE))
        log_base_tex = always_redraw(lambda : MathTex(round(log_base_anim.get_value(), 2)).move_to(math_def[5]).set_color(RED))

        def func_1(log_base, asymptote):

            return lambda x : np.log(x - asymptote) / np.log(log_base)
        
        def lower_limit_value(log_base, asymptote, m):

            return asymptote + np.exp(m * np.log(log_base))
        
        def upper_limit_value(log_base, asymptote, M):

            return min(9, asymptote + np.exp(M * np.log(log_base)))
        
        def required_domain(log_base, asymptote, m, M):
            
            return [lower_limit_value(log_base, asymptote, m), upper_limit_value(log_base, asymptote, M), 0.01]
        
        graph_pic = always_redraw(lambda : ax.plot(func_1(log_base_anim.get_value(), asymptote_anim.get_value()),
                                                   x_range = required_domain(log_base_anim.get_value(), asymptote_anim.get_value(), -5, 5),
                                                   color=YELLOW).set_z_index(-1))

        def graph_label_tex(logBase, asymp):

            curr_tex = MathTex(r"y = f(x)").next_to(ax.c2p(upper_limit_value(logBase, asymp, 5),
                                                                                 func_1(logBase, asymp)(upper_limit_value(logBase, asymp, 5)), 0), RIGHT)
            curr_tex[0][0].set_color(YELLOW)
            curr_tex[0][4].set_color(YELLOW)

            return curr_tex

        graph_label = always_redraw(lambda : graph_label_tex(log_base_anim.get_value(), asymptote_anim.get_value()))

        color_text(y_list = [],
                   g_list = [],
                   r_list = [],
                   b_list = [],
                   formula = graph_label)
        
        VGroup(ax, axes_labels, ax_origin, graph_pic, graph_label
               ).move_to(diagram_position.get_center())
        
        math_def_2 = MathTex(r"\ln(x-c)").move_to(math_def[1])
        math_def_2[0][3].set_color(YELLOW)
        math_def_2[0][5].set_color(BLUE)
        
        self.play(Write(header))
        self.wait()
        
        self.play(Write(math_def[0]))
        self.play(Write(math_def_2))
        self.wait()

        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()
        
        self.play(Write(math_def[2]))
        self.play(Write(asymptote_tex))
        self.wait()

        def asymptote_func(asymp):

            texTerm = VGroup(DashedLine(ax.c2p(asymp, -5, 0), ax.c2p(asymp, 5, 0)),
                                         MathTex(r"x = ", round(asymp, 2)).next_to(ax.c2p(asymp, -5, 0), DOWN)).set_color(BLUE)
            

            return texTerm
        
        asymptote = always_redraw(lambda : asymptote_func(asymptote_anim.get_value()))
        self.play(Write(asymptote))
        self.wait()

        self.play(asymptote_anim.animate.set_value(3), run_time = 3)
        self.wait()
        self.play(asymptote_anim.animate.set_value(-1), run_time = 5)
        self.wait()

        self.play(Write(math_implications[0]), run_time = 2)
        self.wait()
        self.play(asymptote_anim.animate.set_value(1), run_time = 2)
        self.wait()

        self.play(Transform(header, header_2),
                  Transform(math_def_2, math_def[1]),
                  run_time = 2)
        self.wait()

        self.play(Write(math_def[4]))
        self.play(Write(log_base_tex))
        self.wait()

        self.play(log_base_anim.animate.set_value(5), run_time = 3)
        self.wait()
        self.play(log_base_anim.animate.set_value(1.5), run_time = 3)
        self.wait(2)

        self.play(Write(math_implications[1]), run_time = 2)
        self.wait()
        
        self.play(Write(math_implications[2]), run_time = 2)
        self.wait()
        self.wait(5)

    pass

class Absolute(ZoomedScene):

    def construct(self):

        self.camera.frame.scale(1.2)

        header_position = MathTex(r"H").shift(8*LEFT + 3.25*UP)
        diagram_position = MathTex(r"D").shift(4*LEFT + .5*DOWN)
        math_position = MathTex(r"M").shift(4*RIGHT + .5*DOWN)
        
        header = MathTex(r"\underline{19.\ \text{Absolute value function}}").scale(1.2).next_to(header_position, RIGHT)
        
        header_2 = MathTex(r"\underline{20.\ \text{Piecewise function}}").scale(1.2).next_to(header_position, RIGHT)

        math_def = MathTex(r"f(x) &= |x| ",
                           r":= \begin{cases} x & \text{if $x \geq 0$,}\\ -x & \text{if $x < 0$.} \end{cases}",
                           tex_template = myTemplate)
        
        color_text(r_list = [],
                   g_list = [],
                   y_list = [(0, 2, 1), (0, 6, 1),
                             (1, 5, 1), (1, 8, 1),
                             (1, 13, 1), (1, 16, 1), ],
                   b_list = [],
                   formula = math_def)
        
        math_implications = MathTex(r"1.\quad & \text{$|x| \geq 0$}\\ ",
                                r"2.\quad & \text{$|x| = 0 \quad \To \quad x = 0$}\\ ",
                                r"3.\quad & \text{$|kx| = |k||x|,\quad k \in \RR$}\\ ",
                                r"4.\quad & \text{$|a+b| \leq |a| + |b|$}\\ ",
                                r"5.\quad & \text{Real analysis}\\ ",
                                tex_template = myTemplate).scale(.9)
        
        
        color_text(r_list = [(3, 3, 1), (3, 9, 1), ],
                   g_list = [(3, 5, 1), (3, 13, 1), ],
                   y_list = [(0, 3, 1), 
                             (1, 3, 1), (1, 8, 1), 
                             (2, 4, 1), (2, 11, 1), ],
                   b_list = [(2, 3, 1), (2, 8, 1), (2, 14, 1), ],
                   formula = math_implications)
        
        math_implications.next_to(math_def, DOWN, buff = 1)

        VGroup(math_def, math_implications).move_to(math_position)
        
        ax = Axes(
            x_range=[-2.7, 2.7],
            y_range=[-0.7, 2.7],
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": False},
            x_length=7*.75,
            y_length=4.25*.75,
        )
        
        axes_labels = ax.get_axis_labels(x_label=MathTex(r"x").set_color(YELLOW), y_label=MathTex(r"y").set_color(YELLOW))
        axes_labels[0].next_to(ax.get_axis(0), RIGHT)
        axes_labels[1].next_to(ax.get_axis(1), UP)

        ax_origin = MathTex(r"O").scale(.8).next_to(ax.coords_to_point(0,0,0), DL, buff=.15)

        self.wait()

        def func_1():

            return lambda x : x if x >= 0 else -x

        graph_pic = always_redraw(lambda : ax.plot(func_1(), x_range=[-2.2, 2.2, 0.01], color=YELLOW).set_z_index(-1))

        graph_label = MathTex(r"y = f(x)").next_to(ax.c2p(2.2, func_1()(2.2), 0), UP)
        graph_label[0][0].set_color(YELLOW)
        graph_label[0][4].set_color(YELLOW)
        
        VGroup(ax, axes_labels, ax_origin, graph_label, graph_pic
               ).move_to(diagram_position.get_center())
        
        self.play(Write(header))
        self.wait()
        
        self.play(Write(math_def[0]))
        self.wait()
        self.play(Write(math_def[1]))
        self.wait()
        
        self.play(Write(VGroup(ax, axes_labels, ax_origin)))
        self.wait()

        self.play(Write(graph_pic), run_time = 2)
        self.play(Write(graph_label))
        self.wait()
        
        ### math-implications

        for k in range(len(math_implications)):

            self.play(Write(math_implications[k]), run_time = 2)
            self.wait()
        
        self.wait(5)

        ### change to piecewise

        self.play(Circumscribe(math_def, fade_out = True, buff = .15), run_time = 1.5)
        self.wait()

        self.play(Transform(header, header_2), run_time = 1.5)
        self.wait()

        self.wait(5)

        ### which is a really bizarre function, just like these functions that you need to know for college calculus

        pass

    pass

class Thumbnail(MovingCameraScene):

    def construct(self):
        
        warning_sign = MathTex(r"f(x)")
        warning_sign[0][2].set_color(YELLOW)
        
        warning_tex = MathTex(r"\times\ \! 20").set_color(YELLOW).scale(1.2).next_to(warning_sign, RIGHT)
        VGroup(warning_sign, warning_tex).scale(4).move_to(ORIGIN)

        self.add(warning_sign)
        self.add(warning_tex)

        pass