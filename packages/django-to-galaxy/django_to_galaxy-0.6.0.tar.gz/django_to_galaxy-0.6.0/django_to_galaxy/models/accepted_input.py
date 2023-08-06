from django.db import models


class Format(models.Model):
    format = models.CharField(max_length=200, unique=True)
    """Format on the galaxy side."""


class WorkflowInput(models.Model):
    galaxy_step_id = models.IntegerField(null=False)
    """Step id on the galaxy side."""
    workflow = models.ForeignKey("Workflow", null=False, on_delete=models.CASCADE)
    """Workflow id."""
    formats = models.ManyToManyField("Format")
    """Accepted input formats on the galaxy side."""
    optional = models.BooleanField(default=False)
    """Workflow input optional information on the galaxy side."""
