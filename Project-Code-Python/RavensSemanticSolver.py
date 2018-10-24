from abc import ABCMeta, abstractproperty

from RavensSemanticRelationship import AddKeepDelete2x2, SidesArithmetic


class RavensSemanticSolverFactory:
    def __init__(self):
        pass

    def create(self, problem_type):
        """
        Creates an instance of a RavensSemanticSolver for the given problem type.

        :param problem_type: The problem type, either '2x2' or '3x3'.
        :type problem_type: str
        :return: A RavensSemanticSolver.
        :rtype: RavensSemanticSolver
        """
        if problem_type == '2x2':
            return _RavensSemantic2x2Solver()
        elif problem_type == '3x3':
            raise ValueError('3x3 problems are not supported!')
        else:
            raise ValueError('Invalid problem type: {}'.format(problem_type))


class RavensSemanticSolver:
    __metaclass__ = ABCMeta

    def run(self, problem):
        """
        Runs this solver to find an answer to the given problem.

        :param problem: The RPM problem to solve.
        :type problem: RavensVisualProblem.RavensVisualProblem
        :return: The index of the selected answer, or None if no answer could be chosen.
        :rtype: int
        """
        # Since the semantic relationships are more computationally expensive, generate and test one by one
        for relationship in self._relationships:
            answers = []

            for axis in [0, 1]:
                expected = relationship.generate(problem.matrix, axis)
                answer = relationship.test(expected, problem.matrix, problem.answers, axis)
                answers.append(answer)

            # If the answers match from both of the semantic relationships generated by axis,
            # then take this answer as the desired one and stop evaluating any other relationships
            if len(set(answers)) == 1:
                return answers[0]

        return None

    @abstractproperty
    def _relationships(self):
        # The list of all available semantic relationships for this solver
        pass


class _RavensSemantic2x2Solver(RavensSemanticSolver):
    @property
    def _relationships(self):
        return [
            AddKeepDelete2x2(),
            SidesArithmetic()
        ]