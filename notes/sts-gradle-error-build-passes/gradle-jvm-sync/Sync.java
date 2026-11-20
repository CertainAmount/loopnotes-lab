import org.gradle.tooling.*;
import org.gradle.tooling.model.GradleProject;
import java.io.File;
// Mimics an IDE sync: a phased build action over the Tooling API, with the Gradle JVM set by the IDE (setJavaHome).
public class Sync {
  public static class Loaded implements BuildAction<String> {
    public String execute(BuildController c) { return c.getBuildModel().getRootProject().getName(); }
  }
  public static class Finished implements BuildAction<String> {
    public String execute(BuildController c) { return c.getModel(GradleProject.class).getName() + " (" + c.getModel(GradleProject.class).getTasks().size() + " tasks)"; }
  }
  public static void main(String[] a) throws Exception {
    GradleConnector gc = GradleConnector.newConnector().forProjectDirectory(new File(a[0]));
    try (ProjectConnection pc = gc.connect()) {
      pc.action().projectsLoaded(new Loaded(), x -> {}).buildFinished(new Finished(), x -> System.out.println("model root project: " + x)).build()
        .setJavaHome(new File(a[1])).setStandardOutput(System.out).setStandardError(System.out).run();
      System.out.println("SYNC OK");
    } catch (Exception e) {
      System.out.println("SYNC FAILED");
      for (Throwable t = e; t != null; t = t.getCause()) System.out.println((t == e ? "" : "Caused by: ") + t);
    }
  }
}
