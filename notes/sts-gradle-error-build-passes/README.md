# Why does Eclipse or STS show "cannot be resolved to a type" when `./gradlew build` passes, and what do you try after Refresh Gradle Project?

Research note for the loopnotes.dev post `sts-gradle-error-build-passes`. Everything here was gathered on 2026-11-18: an English search-results check, a reading of the official Gradle, Buildship, Eclipse, Lombok and Spring Tools pages, four Korean searches on Naver, and a reproduction of four cases on our own machine (section 4). Other people's posts are listed as links with a one-line summary; their claims are their reports, not our measurements.

## Conclusions

- Project → Clean cannot clear the stale-model case: compiled against the Gradle model from before a dependency change, the code fails with `StringUtils cannot be resolved to a type`; deleting the output and compiling again against the same model fails the same way; the model fetched after the change compiles. Refreshing the Gradle project is what replaces the model.
- The marker text alone does not tell the cases apart. `X cannot be resolved to a type` came from a stale model, from a generated class (MapStruct `CarMapperImpl`) and from a JDK class above the project's Java level (`SequencedCollection`); `is undefined for the type` came from a Lombok getter and from a JDK method (`List.getFirst()`). What separates them is which type the marker names.
- Two of those cases are not fixed by any refresh: the Lombok case (the Lombok jar is already on the refreshed classpath; the compiler needs the Lombok agent) and the generated-class case (the model Buildship imports lists `src/main/java` only, not `build/generated`, and Buildship's source has no annotation-processing setup). The Java-level case is fixed by a refresh when `build.gradle` sets the version: the re-fetched model carried source level 21 instead of 17.
- The answers that rank for this error in English are mostly 2015-2019 forum threads, and two of their tips are out of date: Buildship stopped running a Gradle sync on F5 in 1.0.11, so pressing F5 (or waiting for the editor to catch up) does not refresh the Gradle classpath; run Gradle > Refresh Gradle Project instead.
- "Eclipse never re-reads build.gradle on its own" (2015 forum) stopped being true with Buildship 2.2.0, which added an opt-in automatic sync when build scripts change, so the reader has a real choice between automatic sync and one manual refresh.
- Gradle's own Eclipse plugin page (docs version 9.9.1) says the `eclipse` and `cleanEclipse` tasks are deprecated and will be removed in Gradle 10, and that modern Eclipse imports Gradle projects through Buildship, so generating `.classpath` with `gradle eclipse` (still suggested in top answers) is the wrong next step; the `eclipse { }` block in `build.gradle` is not deprecated and Buildship still reads it.
- In Korean developer posts, Refresh Gradle Project is the usual fix after adding a dependency (9 of the 14 relevant posts we classified); in the 5 posts where it did not help, the causes named were a `rootProject.name` that differs from the Eclipse project name (2), a Java version that differs between Gradle and Eclipse (1), generated sources such as QueryDSL Q classes (1) and damaged workspace metadata (1). After a refresh that changes nothing, compare the project name and the Java level before deleting the workspace or re-importing.

## 1. English search results (2026-11-18)

Queries: "eclipse cannot be resolved to a type but gradle build works from command line", "eclipse refresh gradle project not working", "eclipse gradle project shows errors but gradlew build succeeds spring boot".

What ranks: discuss.gradle.org threads from 2015-2019, Stack Overflow (often through mirror sites), an Eclipse JDT mailing-list post, a Gradle issue (GRADLE-1703), and Elastic and Minecraft Forge forum threads. No official documentation page and no recent first-hand post ranked for these queries.

| Result | Year | What it says | How it ends |
|---|---|---|---|
| [Stack Overflow answer 31256840](https://stackoverflow.com/a/31256840) | — | Project > Clean usually fixes it; problems start when metadata is generated with `gradle eclipse` | Recommends Clean |
| [discuss.gradle.org/t/19082](https://discuss.gradle.org/t/19082) | 2016 | Run `assemble`, then refresh so Eclipse picks up generated source folders (about 700-750 words, 8 replies) | Not solved |
| [discuss.gradle.org/t/13366](https://discuss.gradle.org/t/13366) | 2015 | Neither Buildship nor the STS Gradle plugin refreshes automatically when the build file changes; press F5 (about 700 words, 9 replies) | Ended on a different cause (a DTD) |

Questions none of these three answer: what to do when Refresh Gradle Project leaves the markers in place, and how to tell the cases apart from the marker text.

Google autocomplete on the same day showed demand coming in through the error string ("cannot be resolved to a type eclipse" with string / httpservlet / springbootapplication / autowired / jframe / file / test / applicationcontext) and through "eclipse refresh gradle project not working", "eclipse gradle refresh not working" and "eclipse gradle dependencies not updating".

## 2. Official pages compared with the forum answers

| Page | Read | What it establishes | Forum answer it corrects |
|---|---|---|---|
| [Gradle docs, Eclipse plugin](https://docs.gradle.org/current/userguide/eclipse_plugin.html) | 2026-11-18, page opened (docs version 9.9.1) | "The tasks listed in this section are deprecated and will be removed in Gradle 10." "Modern versions of Eclipse import Gradle projects directly via Buildship without needing these generated files." The `eclipse { }` DSL "is not deprecated and continues to be consumed by Buildship during Gradle import." No mention of generated sources or annotation processing. | Stack Overflow 31256840 and mirrors still point readers at `gradle eclipse` |
| [Buildship 1.0.11 is now available](https://discuss.gradle.org/t/buildship-1-0-11-is-now-available/15482) | 2026-11-18, page opened (post dated 2016-03-29) | "Buildship no longer runs the synchronization between Gradle and Eclipse when you refresh the Eclipse file system (pressing F5)." | discuss.gradle.org/t/13366 (2015): "press F5" |
| [Buildship 2.2.0 is now available](https://discuss.gradle.org/t/buildship-2-2-0-is-now-available/25074) | 2026-11-18, page opened (post dated 2017-12-11) | "Eclipse can be configured to automatically execute Gradle project synchronization when a build script changes. The feature can be enabled in the import wizard or in the workspace and project preferences." | discuss.gradle.org/t/13366 (2015): no automatic refresh |
| [Eclipse Foundation newsletter, Build Gradle projects with Eclipse Buildship (Feb 2018)](https://www.eclipse.org/community/eclipse_newsletter/2018/february/buildship.php) | 2026-11-18, snippet re-checked | "Gradle > Refresh Gradle Project command from the context menu of the project node or the build script editor" | — (menu location) |
| [Spring Tools](https://spring.io/tools) | 2026-11-18, page opened | Current release Spring Tools for Eclipse 5.4.0, built on Eclipse 4.41 (download file names `spring-tools-for-eclipse-5.4.0.RELEASE-e4.41.0-*`); 5.4.0 announced 2026-09-09 ([release post](https://spring.io/blog/2026/09/09/spring-tools-5-4-0-released), snippet) | — (version baseline) |
| [Buildship 3.1.12 is now available](https://discuss.gradle.org/t/buildship-3-1-12-is-now-available/52206) | 2026-11-18, search snippet | Latest Buildship, announced 2026-09-15 | — (version baseline) |
| [Eclipse help, Factory Path preferences](https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/reference/ref-apt-factoryPath.htm) | 2026-11-18, page opened | "Settings in the Factory Path preference pane will only have an effect if annotation processing is enabled in the Annotation Processing preference pane." Processor jars are added with Add External Jars... | — (generated-sources case) |
| [Buildship source, master branch](https://github.com/eclipse/buildship) | 2026-11-18, source read (commit d89b918) | Classpath container label `ClasspathContainer_Label=Project and External Dependencies`; workbench preference page named "Gradle" (`org.eclipse.ui.preferencePages`) carries the checkbox `Preference_Label_AutoSync=Automatic Project Synchronization`, which also appears in the import wizard and the project preference page; no annotation-processing or Factory Path code outside tests | Naver post (windrose1, 2022) was the only source for the container label |
| [Project Lombok, Eclipse setup](https://projectlombok.org/setup/eclipse) | 2026-11-18, page opened | Lists Spring Tools Suite as supported; running `lombok.jar` starts an installer that finds Eclipse installations; "You need to actually quit Eclipse and start it again; the regular restart is not good enough." The page does not say where the installer writes; see section 4, case L. | — |

## 3. Korean developer reports on Naver (2026-11-18)

Four searches, blog / cafe / Q&A (kin), relevance sort, top 25 per type.

| Search term (Korean) | Meaning | Blog | Cafe | kin | Relevant to this symptom |
|---|---|---|---|---|---|
| sts gradle cannot be resolved to a type | the English error string | 3 | 1 | 0 | 1 (the Korean original of this article) |
| 이클립스 gradle 빌드는 되는데 에러 | "Eclipse: Gradle build works but errors" | 218 | 10 | 4 | 2 in the blog top 25, 0-1 in kin |
| sts lombok gradle 인식 안됨 | "STS doesn't recognise Lombok with Gradle" | 8 | 0 | 0 | mostly Lombok installation steps (`lombok.jar`, `-javaagent`) |
| Refresh Gradle Project 안됨 | "Refresh Gradle Project doesn't work" | 77 | 1 | 5 | see the breakdown below |

Hand classification of the last search (blog top 25 plus the cafe and kin results that concern Eclipse or STS), with the QueryDSL post from the second search added: 14 relevant posts. 9 say "after adding a dependency, Refresh Gradle Project fixed it". 5 say Refresh did not fix it and name another cause:

| Cause named | Posts | Post (date, link, one line) |
|---|---|---|
| `settings.gradle` `rootProject.name` differs from the Eclipse project name | 2 | 2022-05 [blog.naver.com/windrose1/222744692164](https://blog.naver.com/windrose1/222744692164): "Project and External Dependencies" missing until the names matched, then refresh rebuilt it. 2023-02 [blog.naver.com/pyk6598/223016581948](https://blog.naver.com/pyk6598/223016581948): "if `rootProject.name` and the Eclipse project name differ, Gradle refresh doesn't work." |
| Gradle builds on Java 21, Eclipse set differently | 1 | 2026-02 [blog.naver.com/elkiss/224180426909](https://blog.naver.com/elkiss/224180426909): aligned Eclipse with the Gradle Java version, then a full refresh and build. |
| Generated sources (QueryDSL `build/generated`) | 1 (2 counting the 2021 post) | 2025-05 [exhibitlove.tistory.com/651](https://exhibitlove.tistory.com/651): Q classes under `build/generated` not seen by Eclipse. 2021-07 [pamyferret.tistory.com/11](https://pamyferret.tistory.com/11): "Q class cannot be resolved" in Eclipse. |
| Damaged workspace `.metadata` | 1 | 2024-08 [oh-rot-ha-da.tistory.com/285](https://oh-rot-ha-da.tistory.com/285): Clean, Refresh and re-import all failed; deleting and rebuilding `.metadata` fixed it. |

Examples of the "Refresh fixed it" group: [lifove.tistory.com/57](https://lifove.tistory.com/57) (2016), [blog.naver.com/kimnew8376/222811353354](https://blog.naver.com/kimnew8376/222811353354) (2022), [blog.naver.com/simpleandminimal/223490882483](https://blog.naver.com/simpleandminimal/223490882483) (2024), [blog.naver.com/hyy127/223965733072](https://blog.naver.com/hyy127/223965733072) (2025).

The other relevant post in the second search: 2026-06 [blog.naver.com/kin412/224324036463](https://blog.naver.com/kin412/224324036463), conflicts when Eclipse's `.classpath` is committed to git.

What stands out: Korean posts repeat Refresh Gradle Project as the step to take after adding a dependency, and the project-name mismatch appears as a "refresh didn't help" cause there but not in the English top results.

## 4. Reproductions on this machine (2026-11-18)

Question: for each cause of "terminal build passes, editor red", which error does the Eclipse compiler give, and does re-fetching the Gradle model (what Refresh Gradle Project does) clear it?

Method: no Eclipse GUI here. Instead, the two inputs Eclipse uses: the Gradle Tooling API `EclipseProject` model (the model Buildship receives on a sync; we dumped its project name, Java source settings, source directories and classpath) and ECJ, the Eclipse batch compiler. Each case is a minimal `java` project (not a Spring Boot one) that `./gradlew clean build` builds successfully. A dump taken before the change stands for the model STS still holds; a dump taken after stands for the refreshed model. Annotation processing is off (`-proc:none`) unless the row says otherwise, matching a JDT project with no annotation-processing setup.

Versions: Gradle 9.8.2 (wrapper), Temurin JDK 21.0.13, ECJ 3.46.100 (Maven Central `org.eclipse.jdt:ecj`), Gradle Tooling API 9.8.2 (repo.gradle.org), Lombok 1.18.48, MapStruct 1.6.3, commons-lang3 3.20.0, Linux.

| Case | Change | ECJ against the old model | ECJ against the re-fetched model | What cleared it |
|---|---|---|---|---|
| E1 stale model | added `implementation 'org.apache.commons:commons-lang3:3.20.0'` and used `StringUtils` | `The import org.apache cannot be resolved`; `StringUtils cannot be resolved to a type` (field); `StringUtils cannot be resolved` (static call). Deleting the output and compiling again (= Project → Clean): the same 3 errors | compiles, 0 errors (classpath now lists the commons-lang3 jar) | the re-fetched model |
| E2a generated class | MapStruct `@Mapper` interface, code calls `new CarMapperImpl()`; Gradle generates it under `build/generated/sources/annotationProcessor/java/main` | — | `CarMapperImpl cannot be resolved to a type`; the model's source directories are `src/main/java` only | the processor on the compiler's processor path (= annotation processing on + Factory Path entry): `CarMapperImpl.java` generated, compiles |
| E2b Lombok | `@Getter` class `Person`, `@Slf4j` class calling `log.info(p.getName())`; Lombok as `compileOnly` + `annotationProcessor` | — | `log cannot be resolved`; `The method getName() is undefined for the type Person` (the Lombok jar is on the model classpath) | running ECJ with `-javaagent:lombok.jar=ECJ` (= Lombok installed into the IDE): compiles |
| E3 Java level | `build.gradle` from `sourceCompatibility = 17` to `toolchain { languageVersion = 21 }`; code uses `SequencedCollection` and `List.getFirst()` | old model: source level 17. ECJ `--release 17`: `The import java.util.SequencedCollection cannot be resolved`; `SequencedCollection cannot be resolved to a type`; `The method getFirst() is undefined for the type List<String>` | re-fetched model: source level 21; ECJ `--release 21` compiles | the re-fetched model |
| E4 project name | `rootProject.name = 'demo-api'` in a folder named `e1` | — | the model's project name is `demo-api` | (Buildship's renaming behaviour needs the GUI; not reproduced) |
| L Lombok installer | `java -jar lombok.jar install <folder>` against a mock STS folder holding `SpringToolSuite4` and `SpringToolSuite4.ini` | — | — | installer printed "Lombok installed to: …/SpringToolSuite4", appended `-javaagent:<folder>/lombok.jar` as the last line of `SpringToolSuite4.ini` and copied `lombok.jar` into the folder |

Notes: in E2a, passing the processor jar through ECJ's `-processorpath` did not load the processor in this run (`ClassNotFoundException` with an explicit `-processor`); placing it on the classpath, where ECJ discovers it through `META-INF/services`, worked. All Gradle daemons were stopped after the runs.

## Limits

- The sample is small: 14 relevant posts, classified by hand from search snippets and titles. Read the counts as which causes come up, not how often each happens.
- The Naver reports are other developers' accounts; we did not reproduce the project-name or `.metadata` cases.
- The Buildship 3.1.12 row is based on a search snippet read on 2026-11-18, not on the full page.
- The reproductions use the model Buildship receives and the Eclipse batch compiler, not a running STS, so they show the compiler's error text and what each model contains, not the editor's behaviour (for example how quickly markers update). The projects are plain Gradle `java` projects, not Spring Boot ones.
- Search results and autocomplete are a single day's snapshot (2026-11-18) and change over time.

## 5. Settings named in the article's fix steps (2026-11-18, reader fix)

| Page | Read | What it establishes |
|---|---|---|
| [Eclipse help, Annotation Processing preferences](https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/reference/ref-apt-config.htm) | 2026-11-18, page opened | "Annotation processing is turned off by default, and must be turned on by checking this checkbox for each project that needs it." Generated files go to `.apt_generated` by default. |
| [JDT APT UI plugin.xml](https://github.com/eclipse-jdt/eclipse.jdt.core/blob/master/org.eclipse.jdt.apt.ui/plugin.xml) and plugin.properties, master | 2026-11-18, source read | The Annotation Processing property page sits under the Java Compiler page (`category="org.eclipse.jdt.ui.propertyPages.CompliancePreferencePage"`), and Factory Path sits under Annotation Processing; checkbox label `Enable annotation processing` (`AptConfigurationBlock_enable`). |
| [Eclipse help, Factory Path preferences](https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/reference/ref-apt-factoryPath.htm) | 2026-11-18, page opened | Processor jars are added by absolute path with Add External Jars... |
| [Eclipse help, Java Compiler property page](https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/reference/ref-properties-compiler.htm) and [Java Compiler preferences](https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/reference/preferences/java/ref-preferences-compiler.htm) | 2026-11-18, pages opened | Reached from the project's Properties → Java Compiler; "Enable project specific settings" allows per-project values; the JDK Compliance group has "Compiler compliance level". |
| [Buildship CoreMessages.properties](https://github.com/eclipse/buildship/blob/master/org.eclipse.buildship.core/src/main/resources/org/eclipse/buildship/core/internal/i18n/CoreMessages.properties), master | 2026-11-18, source read | Labels on the Gradle preference page: `Gradle distribution` group with the option `Gradle wrapper`; `Java home`; `Automatic Project Synchronization` ("Automatically start project synchronization in the background when the build script changes."). |
| `gradle --version` on this machine | 2026-11-18, Gradle 9.8.2 run with Temurin 21.0.13 | Prints `Launcher JVM:  21.0.13 (Eclipse Adoptium 21.0.13+9-LTS)` and `Daemon JVM: <path> (no Daemon JVM specified, using current Java home)`; the Launcher JVM line carries the version number. |

Moved from the article body (reader fix r1): the reproduction was run by Claude Code on the author's machine with ECJ and the Tooling API model (method in section 4); the article keeps only its conclusion (Clean recompiles against the same stale model and fails the same way). The `rootProject.name` check came from Korean developer posts (section 3); the article states the check without that framing.

## 6. Steps added on the second reader fix (2026-11-18)

| Page | Read | What it establishes |
|---|---|---|
| [Project Lombok, Eclipse setup](https://projectlombok.org/setup/eclipse) and [download page](https://projectlombok.org/download) | 2026-11-18, pages opened | `lombok.jar` is "downloadable from this site, or from your maven repository; it's the same jar". The setup page says the installer finds Eclipse installations (Spring Tools Suite listed), and that you must quit and start again. |
| [Lombok installer source, InstallerGUI.java](https://github.com/projectlombok/lombok/blob/master/src/installer/lombok/installer/InstallerGUI.java), master (commit effbae9) | 2026-11-18, source read | Buttons `Specify location...` and `Install / Update`; when no IDE is found the installer says to use 'Specify Location...' to point at the IDE installation by hand. |
| [Buildship UI plugin.xml](https://github.com/eclipse/buildship/blob/master/org.eclipse.buildship.ui/plugin.xml), master | 2026-11-18, source read | Import wizard `Existing Gradle Project` in the `Gradle` import category; command `Add Gradle Nature` contributed to the project's Configure menu (`popup:org.eclipse.ui.projectConfigure`) and shown only for projects without the Gradle nature; the `Gradle` context menu carries `Refresh Gradle Project`. |
| [Eclipse help, Annotation Processing preferences](https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/reference/ref-apt-config.htm) | 2026-11-18 (section 5) | Generated files go to the Generated source directory, `.apt_generated` by default. |

Moved from the article body (reader fix r2): the sentence reporting the E1 reproduction ("the model from before the dependency change failed with `StringUtils cannot be resolved to a type` before and after a clean, and the model fetched after the change compiled cleanly"); the body keeps the conclusion that Clean recompiles against the same model and fails the same way. Section 4, row E1 holds the run. The minutes the author spent rereading `build.gradle` stay out of the body; the body keeps that he reread it with the terminal green.

## 7. Steps added on the third reader fix (2026-11-18)

| Page | Read | What it establishes |
|---|---|---|
| Gradle module cache on this machine (`~/.gradle/caches/modules-2/files-2.1/org.mapstruct/`) | 2026-11-18, listed | The processor jar sits at `mapstruct-processor/1.6.3/<sha1 folder>/mapstruct-processor-1.6.3.jar`: one hash-named folder below the version folder, so a `find ... -name 'mapstruct-processor-*.jar'` finds it faster than browsing. |
| [querydsl-apt 5.1.0 POM](https://repo1.maven.org/maven2/com/querydsl/querydsl-apt/5.1.0/querydsl-apt-5.1.0.pom) and [querydsl-codegen 5.1.0 POM](https://repo1.maven.org/maven2/com/querydsl/querydsl-codegen/5.1.0/querydsl-codegen-5.1.0.pom), Maven Central | 2026-11-18, read | `querydsl-apt` depends on `querydsl-codegen` (compile), which brings `querydsl-core`, `codegen-utils`, `javax.inject` and `classgraph`; a Factory Path holding only the `querydsl-apt` jar would miss them. Not reproduced in an IDE; the article points the reader to `./gradlew dependencies --configuration annotationProcessor` for the list. |
| Reproduction E3 (section 4) | 2026-11-18 | With the compliance level matching the Gradle Java version (ECJ `--release 21`), the code using `SequencedCollection` and `List.getFirst()` compiles: the marker clears after the rebuild. |

Moved from the article body (reader fix r3): the list step "Reran `./gradlew clean build` in the terminal, in case old build output had carried the first pass" is now one clause in the scene sentence; the reason for the rerun (ruling out old build output) stays in the Korean source and here.

Article: ['STS "cannot be resolved to a type" but Gradle build passes'](https://loopnotes.dev/sts-gradle-error-build-passes/)
